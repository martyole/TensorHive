import tensorflow as tf
from utils import build_and_compile_cnn_model, prepare_train_datasets
from absl import flags, app

FLAGS = flags.FLAGS

flags.DEFINE_integer('batch_size', 64, 'Batch size', lower_bound=0)
flags.DEFINE_integer('epochs', 3, 'Number of epochs', lower_bound=0)
flags.DEFINE_integer('steps_per_epoch', 500, 'Number of steps in each epoch', lower_bound=0)
flags.DEFINE_integer('task_index', 0, 'Index of task within the job', lower_bound=0)
flags.DEFINE_string('ps_hosts', '', 'Comma-separated list of hostname:port pairs')
flags.DEFINE_string('worker_hosts', '', 'Comma-separated list of hostname:port pairs')
flags.DEFINE_string('job_name', '', 'One of ps, worker')


def main(argv):
    ps_hosts = FLAGS.ps_hosts.split(",") if len(FLAGS.ps_hosts) > 0 else []
    worker_hosts = FLAGS.worker_hosts.split(",") if len(FLAGS.worker_hosts) > 0 else []
    cluster_spec = tf.train.ClusterSpec({"ps": ps_hosts, "worker": worker_hosts})
    cluster_resolver = tf.distribute.cluster_resolver.SimpleClusterResolver(cluster_spec, task_type=FLAGS.job_name,
                                                                            task_id=FLAGS.task_index)

    strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(cluster_resolver=cluster_resolver)
    train_datasets = prepare_train_datasets(FLAGS.batch_size)

    with strategy.scope():
        model = build_and_compile_cnn_model()
    model.fit(x=train_datasets, epochs=FLAGS.epochs, steps_per_epoch=FLAGS.steps_per_epoch)


if __name__ == '__main__':
    app.run(main)
