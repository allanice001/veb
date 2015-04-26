from jadi import component

from vvv.api.template import Template

@component(Template)
class ConfigFileTemplate(Template):
    name = 'nginx.conf'
    data = """
#AUTOMATICALLY GENERATED - DO NO EDIT!

user ${system_config['nginx']['user']} ${system_config['nginx']['user']};
pid /var/run/nginx.pid;
worker_processes ${system_config['nginx']['workers']};
worker_rlimit_nofile 100000;

events {
    worker_connections  4096;
    include /etc/nginx.custom.events.d/*.conf;
}

http {
    default_type application/octet-stream;

    access_log off;
    error_log  ${system_config['log_dir']}/nginx/error.log crit;

    sendfile on;
    tcp_nopush on;

    keepalive_timeout 20;
    client_header_timeout 20;
    client_body_timeout 20;
    reset_timedout_connection on;
    send_timeout 20;

    types_hash_max_size 2048;

    gzip on;
    gzip_disable "msie6";
    gzip_proxied any;
    gzip_min_length 256;
    gzip_comp_level 4;
    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript application/javascript text/x-js;

    server_names_hash_bucket_size 128;

    include mime.conf;
    charset UTF-8;

    open_file_cache max=100000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;

    server_tokens off;

    include proxy.conf;
    include fcgi.conf;

    include conf.d/*.conf;
    include /etc/nginx.custom.d/*.conf;
}

include /etc/nginx.custom.global.d/*.conf;

    """


@component(Template)
class ProxyConfigFileTemplate(Template):
    name = 'nginx.proxy.conf'
    data = """
proxy_redirect          off;
proxy_set_header        Host            $host;
proxy_set_header        X-Real-IP       $remote_addr;
proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
client_body_buffer_size 128k;
proxy_connect_timeout   90;
proxy_send_timeout      90;
proxy_read_timeout      90;
proxy_buffers           32 4k;
"""


@component(Template)
class FCGIConfigFileTemplate(Template):
    name = 'nginx.fcgi.conf'
    data = """
fastcgi_param   QUERY_STRING            $query_string;
fastcgi_param   REQUEST_METHOD          $request_method;
fastcgi_param   CONTENT_TYPE            $content_type;
fastcgi_param   CONTENT_LENGTH          $content_length;

fastcgi_param   SCRIPT_FILENAME         $document_root$fastcgi_script_name;
fastcgi_param   SCRIPT_NAME             $fastcgi_script_name;
fastcgi_param   PATH_INFO               $fastcgi_path_info;
fastcgi_param   REQUEST_URI             $request_uri;
fastcgi_param   DOCUMENT_URI            $document_uri;
fastcgi_param   DOCUMENT_ROOT           $document_root;
fastcgi_param   SERVER_PROTOCOL         $server_protocol;

fastcgi_param   GATEWAY_INTERFACE       CGI/1.1;
fastcgi_param   SERVER_SOFTWARE         nginx/$nginx_version;

fastcgi_param   REMOTE_ADDR             $remote_addr;
fastcgi_param   REMOTE_PORT             $remote_port;
fastcgi_param   SERVER_ADDR             $server_addr;
fastcgi_param   SERVER_PORT             $server_port;
fastcgi_param   SERVER_NAME             $server_name;

fastcgi_param   HTTPS                   $https;

fastcgi_param   REDIRECT_STATUS         200;
"""


@component(Template)
class MIMEConfigFileTemplate(Template):
    name = 'nginx.mime.conf'
    data = """
types {
    text/html                             html htm shtml;
    text/css                              css;
    text/xml                              xml rss;
    image/gif                             gif;
    image/jpeg                            jpeg jpg;
    application/x-javascript              js;
    text/plain                            txt;
    text/x-component                      htc;
    text/mathml                           mml;
    image/png                             png;
    image/svg+xml                         svg svgz;
    image/x-icon                          ico;
    image/x-jng                           jng;
    image/vnd.wap.wbmp                    wbmp;
    application/java-archive              jar war ear;
    application/mac-binhex40              hqx;
    application/pdf                       pdf;
    application/x-cocoa                   cco;
    application/x-java-archive-diff       jardiff;
    application/x-java-jnlp-file          jnlp;
    application/x-makeself                run;
    application/x-perl                    pl pm;
    application/x-pilot                   prc pdb;
    application/x-rar-compressed          rar;
    application/x-redhat-package-manager  rpm;
    application/x-sea                     sea;
    application/x-shockwave-flash         swf;
    application/x-stuffit                 sit;
    application/x-tcl                     tcl tk;
    application/x-x509-ca-cert            der pem crt;
    application/x-xpinstall               xpi;
    application/zip                       zip;
    application/octet-stream              deb;
    application/octet-stream              bin exe dll;
    application/octet-stream              dmg;
    application/octet-stream              eot;
    application/octet-stream              iso img;
    application/octet-stream              msi msp msm;
    audio/mpeg                            mp3;
    audio/ogg                             oga ogg;
    audio/wav                             wav;
    audio/x-realaudio                     ra;
    video/mp4                             mp4;
    video/mpeg                            mpeg mpg;
    video/ogg                             ogv;
    video/quicktime                       mov;
    video/webm                            webm;
    video/x-flv                           flv;
    video/x-msvideo                       avi;
    video/x-ms-wmv                        wmv;
    video/x-ms-asf                        asx asf;
    video/x-mng                           mng;
}
    """

@component(Template)
class WebsiteConfigFileTemplate(Template):
    name = 'nginx.website.conf'
    data = """
#AUTOMATICALLY GENERATED - DO NO EDIT!

${website['custom_conf_toplevel'] or ''}

server {
    % if website['domains']:
    server_name
    % for domain in website['domains']:
        ${domain['domain']}
    % endfor
        ;
    % endif

    % for port in website['ports']:
    listen ${port['host']}:${port['port']}
        % if port['ssl']:
            ssl
        % endif
        % if port['spdy']:
            spdy
        % endif
        % if port['default']:
            default_server
        % endif
        ;
    % endfor

    % if website['ssl_cert_path']:
    ssl_certificate ${website['ssl_cert_path']};
    ssl_certificate_key ${website['ssl_key_path']};
    % endif

    access_log ${system_config['log_dir']}/nginx/${website['name']}.access.log;
    error_log  ${system_config['log_dir']}/nginx/${website['name']}.error.log;

    % if website['root']:
    root ${website['root']};
    % endif

    index index.html index.htm index.php;

    % if not website['maintenance_mode']:
    ${website['custom_conf'] or ''}

    % for location in location_info:
    location ${location['pattern']} ${
        {
            'exact': '',
            'regex': '~',
            'force-regex': '^~',
        }[location['match']]
    } {
        ${location['custom_conf'] or ''}

        % if not location['custom_conf_override']:
            %if location['path_append_pattern']:
                root ${location['path']};
            % endif
            %if not location['path_append_pattern']:
                alias ${location['path']};
            % endif

            % if location['type'] == 'static':
                %if location['params']['autoindex']:
                    autoindex on;
                % endif
            % endif

            % if location['type'] == 'proxy':
                proxy_pass ${location['params']['url']};
                proxy_set_header Host $http_host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header HTTPS $https;
            % endif

            % if location['type'] == 'fcgi':
                fastcgi_index index.php;
                include fcgi.conf;
                fastcgi_pass ${location['params']['url']};
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            % endif

        % endif
    }
    % endfor

    % endif

    % if website['maintenance_mode']:
    location / {
        return 503;
        error_page 503 @maintenance;
    }

    location @maintenance {
        root /var/lib/ajenti/plugins/vh/extras; # TODO
        rewrite ^(.*)$ /maintenance.html break;
    }
    % endif
}

"""


TEMPLATE_LOCATION_CONTENT_PHP_FCGI = """
        fastcgi_index index.php;
        include fcgi.conf;
        fastcgi_pass unix:/var/run/ajenti-v-php-fcgi-%(id)s.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
"""

TEMPLATE_LOCATION_CONTENT_PYTHON_WSGI = """
        proxy_pass http://unix:/var/run/ajenti-v-gunicorn-%(id)s.sock;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
"""

TEMPLATE_LOCATION_CONTENT_RUBY_UNICORN = """
        proxy_pass http://unix:/var/run/ajenti-v-unicorn-%(id)s.sock;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
"""

TEMPLATE_LOCATION_CONTENT_RUBY_PUMA = """
        proxy_pass http://unix:/var/run/ajenti-v-puma-%(id)s.sock;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
"""


TEMPLATE_LOCATION_CONTENT_NODEJS = """
        proxy_pass http://127.0.0.1:%(port)i;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
"""
