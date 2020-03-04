# TensorFlow v1 readme
## Example run config
python train_estimator.py --ps_hosts=des05.kask:2225 --worker_hosts=des06.kask:2225,des07.kask:2225 --task_index=0 --job_name=ps
python train_estimator.py --ps_hosts=des05.kask:2225 --worker_hosts=des06.kask:2225,des07.kask:2225 --task_index=0 --job_name=worker
python train_estimator.py --ps_hosts=des05.kask:2225 --worker_hosts=des06.kask:2225,des07.kask:2225 --task_index=1 --job_name=worker
