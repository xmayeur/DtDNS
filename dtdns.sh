cd ~
docker run -ti --name dtdns -v $(pwd):/conf/ -v /var/log:/var/log/ xmayeur/dtdns:dtdns
# docker stop dtdns &&  docker rm dtdns

