#!/usr/bin/env python3
"""
Stable Server Runner for AI Hadith Authenticator
Bypasses Windows threading issues with alternative server configurations
"""

import os
import sys
import signal
import time
import threading
from app import app

def run_with_waitress():
    """Run with Waitress server (Windows-compatible)"""
    try:
        from waitress import serve
        print("🍽️ Starting with Waitress server (Windows optimized)")
        serve(
            app,
            host='0.0.0.0',
            port=5000,
            threads=4,
            connection_limit=1000,
            cleanup_interval=10,
            channel_timeout=120
        )
    except ImportError:
        print("❌ Waitress not installed. Install with: pip install waitress")
        return False

def run_with_flask():
    """Run with Flask development server"""
    try:
        print("🚀 Starting Flask development server")
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=False,  # Disable reloader to avoid threading issues
            threaded=False  # Disable threading to avoid Windows issues
        )
    except Exception as e:
        print(f"❌ Flask server error: {e}")
        return False
    except Exception as e:
        print(f"❌ Waitress failed: {e}")
        return False
    return True

def run_with_gunicorn():
    """Run with Gunicorn server"""
    try:
        import gunicorn.app.base
        print("🦄 Starting with Gunicorn server")
        from gunicorn.app.base import BaseApplication
        
        class StandaloneApplication(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()
            
            def load_config(self):
                config = {key: value for key, value in self.options.items()
                         if key in self.cfg.settings and value is not None}
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)
            
            def load(self):
                return self.application
        
        options = {
            'bind': '%s:%s' % ('0.0.0.0', '5000'),
            'workers': 1,
            'threads': 4,
            'timeout': 120,
            'keepalive': 2,
            'max_requests': 1000,
            'max_requests_jitter': 50,
            'preload_app': True,
        }
        
        StandaloneApplication(app, options).run()
    except ImportError:
        print("❌ Gunicorn not available")
        return False
    except Exception as e:
        print(f"❌ Gunicorn failed: {e}")
        return False
    return True

def run_with_simple_server():
    """Run with Python's built-in HTTPServer"""
    try:
        from werkzeug.serving import make_server
        print("🔧 Starting with Simple HTTP Server")
        
        # Create server without threading
        server = make_server('0.0.0.0', 5000, app, threaded=False)
        print("🚀 Server running at http://localhost:5000")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Simple server failed: {e}")
        return False
    return True

def run_with_flask_development():
    """Run with Flask development server (minimal config)"""
    try:
        print("🔧 Starting with Flask Development Server (Safe Mode)")
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=False,
            use_reloader=False,
            passthrough_errors=True
        )
    except Exception as e:
        print(f"❌ Flask dev server failed: {e}")
        return False
    return True

def main():
    """Main entry point with fallback options"""
    print("🕌 AI Hadith Authenticator - Stable Server Runner")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Set environment variables for stability
    os.environ.setdefault('WERKZEUG_RUN_MAIN', 'true')
    os.environ.setdefault('FLASK_ENV', 'production')
    
    # Server options in order of preference
    server_options = [
        ("Waitress", run_with_waitress),
        ("Gunicorn", run_with_gunicorn),
        ("Simple Server", run_with_simple_server),
        ("Flask Dev", run_with_flask_development),
    ]
    
    for name, runner in server_options:
        try:
            print(f"\n🔄 Trying {name}...")
            if runner():
                break
            else:
                print(f"⚠️ {name} failed, trying next option...")
        except KeyboardInterrupt:
            print("\n👋 Server stopped by user")
            sys.exit(0)
        except Exception as e:
            print(f"❌ {name} error: {e}")
            continue
    else:
        print("\n❌ All server options failed!")
        print("💡 Try installing Waitress: pip install waitress")
        sys.exit(1)

if __name__ == '__main__':
    # Setup signal handlers
    def signal_handler(signum, frame):
        print(f"\n🛑 Received signal {signum}, shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    main()
