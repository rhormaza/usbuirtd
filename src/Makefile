BIN_DIR = /usr/local/bin
LIB_DIR = /usr/local/lib/usbuirtd
CONF_DIR = /usr/local/etc/usbuirtd
INIT_DIR = /etc/rc.d

CONF_FILES = usbuirtd.conf remotes.conf
INIT_SCRIPT = usbuirtd.sh
DAEMON = usbuirtd.py
OBJS = __init__.py daemon.py tcp_server.py usbuirt.py util.py uuirtdrv.so $(DAEMON)
    
install: ${OBJS} $(DAEMON)
	install -d -m 0755 $(LIB_DIR)
	install -d -m 0755 $(CONF_DIR)
	install -d -m 0755 $(INIT_DIR)
	
	install -m 0755 $(OBJS) $(LIB_DIR)
	install -m 0755 $(CONF_FILES) $(CONF_DIR)
	install -m 0755 $(INIT_SCRIPT) $(INIT_DIR)	
	
	ln -s $(LIB_DIR)/$(DAEMON) $(BIN_DIR)/$(DAEMON)

deinstall: ${OBJS}
	rm -rf $(LIB_DIR)
	rm -rf $(CONF_DIR)
	rm  $(INIT_DIR)/$(INIT_SCRIPT)
	
	rm  $(BIN_DIR)/$(DAEMON)
	
#	rm /var/run/usbuirtd.pid
#	rm /var/log/usbuirtd.log

reinstall :: deinstall
	install -d -m 0755 $(LIB_DIR)
	install -d -m 0755 $(CONF_DIR)
	install -d -m 0755 $(INIT_DIR)
	
	install -m 0755 $(OBJS) $(LIB_DIR)
	install -m 0755 $(CONF_FILES) $(CONF_DIR)
	install -m 0755 $(INIT_SCRIPT) $(INIT_DIR)	
	
	ln -s $(LIB_DIR)/$(DAEMON) $(BIN_DIR)/$(DAEMON)

.PHONY: install deinstall reinstall