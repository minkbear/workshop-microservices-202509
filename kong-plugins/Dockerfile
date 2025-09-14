FROM kong
COPY kong.conf /etc/kong/
USER root
WORKDIR /usr/local/share/lua/5.1/kong/plugins/
COPY . .
RUN cd /usr/local/share/lua/5.1/kong/plugins/demo-auth && luarocks make
USER kong