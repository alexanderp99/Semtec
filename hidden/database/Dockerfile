FROM ontotext/graphdb:11.0.1
#COPY rdf.ttl /root/graphdb-import
COPY ../hidden/microservice1/data/rdf.ttl /opt/graphdb/data/rdf.ttl
COPY ../hidden/microservice1/data/repo-config.ttl /opt/graphdb/data/repo-config.ttl
COPY fill_db.sh /usr/local/bin/
ENV GRAPHDB_HOME=/opt/graphdb/home

# Run the importrdf tool to preload the data
RUN /opt/graphdb/dist/bin/importrdf  \
    -Dgraphdb.inference.buffer=50 \
    -Dgraphdb.inference.concurrency=1 \
    preload \
     -a 5 \
      -b 5 \
    -Dgraphdb.home=$GRAPHDB_HOME \
    -f \
    -c /opt/graphdb/data/repo-config.ttl \
    /opt/graphdb/data/rdf.ttl



# Clean up the original files (optional)
RUN rm /opt/graphdb/data/rdf.ttl /opt/graphdb/data/repo-config.ttl
