docker rm -f dtdns
git pull
chmod +x dtdns.sh
sudo cp dtdns.ini dtdns.sh /root
docker build -t dtdns . && \
docker tag dtdns xmayeur/dtdns
sh ./dtdns.sh &


