docker rm -f dtdns
git pull
sudo cp dtdns.ini dtdns.sh /root
docker build -t dtdns . && \
docker tag dtdns xmayeur/dtdns
sh ./dtdns &


