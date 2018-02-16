cd ~
docker run -ti --name dtdns -v ~:/conf/ dtdns
docker stop dtdns &&  docker rm dtdns

