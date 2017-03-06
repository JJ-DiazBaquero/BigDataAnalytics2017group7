import sys
sys.path.insert(0, '/opt/local/share/python/')
import zorba_api

print "Running: Get zorba instance and shutdown"

store = zorba_api.InMemoryStore_getInstance()
zorba = zorba_api.Zorba_getInstance(store)
zorba.shutdown()
zorba_api.InMemoryStore_shutdown(store)

print "Success"