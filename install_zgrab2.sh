#!/bin/bash
apt-get install git
apt-get install make
wget -c https://storage.googleapis.com/golang/go1.12.5.linux-amd64.tar.gz
tar -C /usr/local/ -xvzf go1.12.5.linux-amd64.tar.gz
mkdir -p ~/go_projects
mkdir -p ~/go_projects/bin
mkdir -p ~/go_projects/src
mkdir -p ~/go_projects/pkg
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
echo 'export GOPATH="$HOME/go_projects"' >> ~/.profile
echo 'GOBIN="$GOPATH/bin"' >> ~/.profile
echo 'alias zgrab2="$GOPATH/src/github.com/zmap/zgrab2/zgrab2"' >> ~/.profile
source ~/.profile
go get github.com/zmap/zgrab2
go get golang.org/x/crypto/curve25519
go get gopkg.in/mgo.v2/bson
go get golang.org/x/text/width
go get golang.org/x/text/unicode/norm
go get golang.org/x/net/http/httpguts
go get golang.org/x/net/http2/hpack
go get golang.org/x/net/idna
cd $GOPATH/src/github.com/zmap/zgrab2
make
cd ~
