start() {
    echo 'Starting services..'
  systemctl start consolidations-processor.service && systemctl is-active --quiet consolidations-processor.service && echo consolidations-processor is running || echo 'consolidations-processor is not running'
  systemctl start rank-processor.service && systemctl is-active --quiet rank-processor.service && echo rank-processor is running || echo 'rank-processor is not running'
  systemctl start scrutineer-processor.service && systemctl is-active --quiet consolidations-processor.service && echo consolidations-processor is running || echo 'consolidations-processor is not running'
}

stop() {
  echo 'Stopping services..'
  systemctl stop consolidations-processor.service && systemctl is-active --quiet consolidations-processor.service && echo 'consolidations-processor is running' || echo 'consolidations-processor is not running'
  systemctl stop rank-processor.service && systemctl is-active --quiet rank-processor.service && echo consolidations-processor is running || echo consolidations-processor is not running
  systemctl stop scrutineer-processor.service && systemctl is-active --quiet scrutineer-processor.service && echo scrutineer-processor is running || echo scrutineer-processor is not running
}

case "$1" in
    start)
       start
       ;;
    stop)
       stop
       ;;
    restart)
       stop
       start
       ;;
    *)
       echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0
