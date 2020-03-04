# TensorFlow v1 readme
## Example run config
```bash
python train.py --ps_hosts=des05.kask:2225 --worker_hosts=des06.kask:2225,des07.kask:2225 --task_index=0 --job_name=ps
python train.py --ps_hosts=des05.kask:2225 --worker_hosts=des06.kask:2225,des07.kask:2225 --task_index=0 --job_name=worker
python train.py --ps_hosts=des05.kask:2225 --worker_hosts=des06.kask:2225,des07.kask:2225 --task_index=1 --job_name=worker
```
