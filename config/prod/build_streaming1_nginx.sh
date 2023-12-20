./configure --add-module=../nginx-rtmp-module --lock-path=/var/run/nginx.lock --pid-path=/run/nginx.pid --with-http_ssl_module --with-pcre=/root/pcre-8.44 --with-zlib=/root/zlib-1.2.11 --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --user=nginx --group=nginx --with-http_auth_request_module --with-http_degradation_module --with-http_geoip_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_image_filter_module --with-http_mp4_module --with-http_perl_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_v2_module --with-stream_ssl_module --with-stream --with-threads --prefix=/usr/local/nginx --with-openssl=/usr/local/openssl
#--prefix=/etc/nginx
#--sbin-path=/usr/sbin/nginx \ 
#--conf-path=/etc/nginx/nginx.conf \