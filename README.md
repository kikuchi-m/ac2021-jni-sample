## JNI sample code for Advent Calendar 2021
[atWare Advent Calendar](https://qiita.com/advent-calendar/2021/atware)

1. `./performance.py prepare`
1. `./performance.py measure`

To measure performance with spacific settings, run with parameters.

```
$ ./performance.py measure --data-size 2000000 --chunk-size 50000 --heap 1024
```

For more detail, `./perfomance.py measure -h`.
