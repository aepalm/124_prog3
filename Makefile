# allow us to get an executable for our partition.py
partiton: partition.py
	cp partition.py partition
	chmod +x partition

clean:
	rm -f partition