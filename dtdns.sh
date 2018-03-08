cd ~
docker run -ti --name dtdns --dns 192.168.0.4 -v $(pwd):/conf/ -v /var/log:/var/log/ xmayeur/dtdns
# docker stop dtdns &&  docker rm dtdns

