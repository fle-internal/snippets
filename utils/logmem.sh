while true; do
	date >> /home/ubuntu/logging/memlog.txt
	top -b -n 1 | head -n 4 >> /home/ubuntu/logging/memlog.txt
	sudo smem | tail -n 10 | sed '1!G;h;$!d' >> /home/ubuntu/logging/memlog.txt
	echo "" >> /home/ubuntu/logging/memlog.txt
        sleep 300
done

