from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow_datasets as tfds
import tensorflow as tf
from absl import flags, app
import os

BUFFER_SIZE = 10000
BATCH_SIZE = 64
LEARNING_RATE = 1e-4

FLAGS = flags.FLAGS

flags.DEFINE_integer('batch_size', 64, 'Batch size', lower_bound=0)
flags.DEFINE_integer('epochs', 3, 'Number of epochs', lower_bound=0)
flags.DEFINE_integer('steps_per_epoch', 500, 'Number of steps in each epoch', lower_bound=0)
flags.DEFINE_integer('task_index', 0, 'Index of task within the job', lower_bound=0)
flags.DEFINE_string('ps_hosts', '', 'Comma-separated list of hostname:port pairs')
flags.DEFINE_string('worker_hosts', '', 'Comma-separated list of hostname:port pairs')
flags.DEFINE_string('job_name', '', 'One of ps, worker')


def input_fn(mode, input_context=None):
    datasets, info = tfds.load(name='mnist',
                               with_info=True,
                               as_supervised=True)
    mnist_dataset = (datasets['train'] if mode == tf.estimator.ModeKeys.TRAIN else
    datasets['test'])

    def scale(image, label):
        image = tf.cast(image, tf.float32)
        image /= 255
        return image, label

    if input_context:
        mnist_dataset = mnist_dataset.shard(input_context.num_input_pipelines,
                                            input_context.input_pipeline_id)
    return mnist_dataset.map(scale).cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE)


def model_fn(features, labels, mode):
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10)
    ])
    logits = model(features, training=False)

    if mode == tf.estimator.ModeKeys.PREDICT:
        predictions = {'logits': logits}
        return tf.estimator.EstimatorSpec(labels=labels, predictions=predictions)

    optimizer = tf.compat.v1.train.GradientDescentOptimizer(
        learning_rate=LEARNING_RATE)
    loss = tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True, reduction=tf.keras.losses.Reduction.NONE)(labels, logits)
    loss = tf.reduce_sum(loss) * (1. / BATCH_SIZE)
    if mode == tf.estimator.ModeKeys.EVAL:
        return tf.estimator.EstimatorSpec(mode, loss=loss)

    logging_hook = tf.estimator.LoggingTensorHook({"loss": loss}, every_n_iter=100)
    return tf.estimator.EstimatorSpec(
        mode=mode,
        loss=loss,
        training_hooks=[logging_hook],
        train_op=optimizer.minimize(
            loss, tf.compat.v1.train.get_or_create_global_step()))


def set_tf_config(task_type, task_index, worker_hosts_string, ps_hosts_string):
    ps_hosts_processed = str(ps_hosts_string.split(",")).replace("'", "\"") if len(ps_hosts_string) > 0 else "[]"
    worker_hosts_processed = str(worker_hosts_string.split(",")).replace("'", "\"") if len(
        worker_hosts_string) > 0 else "[]"
    tf_config = '{"cluster":{"worker":__WORKER_HOSTS,"ps":__PS_HOSTS},"task":{"type":"__TASK_TYPE","index":__TASK_INDEX}}'
    tf_config = tf_config.replace("__TASK_TYPE", task_type)
    tf_config = tf_config.replace("__TASK_INDEX", str(task_index))
    tf_config = tf_config.replace("__WORKER_HOSTS", worker_hosts_processed)
    tf_config = tf_config.replace("__PS_HOSTS", ps_hosts_processed)
    os.environ["TF_CONFIG"] = tf_config


def main(argv):
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)
    set_tf_config(FLAGS.job_name, FLAGS.task_index, FLAGS.worker_hosts, FLAGS.ps_hosts)
    strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
    config = tf.estimator.RunConfig(train_distribute=strategy)

    classifier = tf.estimator.Estimator(
        model_fn=model_fn, model_dir='./tmp/multiworker', config=config)
    tf.estimator.train_and_evaluate(
        classifier,
        train_spec=tf.estimator.TrainSpec(input_fn=input_fn),
        eval_spec=tf.estimator.EvalSpec(input_fn=input_fn)
    )


if __name__ == '__main__':
    app.run(main)
