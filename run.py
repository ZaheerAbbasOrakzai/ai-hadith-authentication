#!/usr/bin/env python3
"""
AI Hadith Authenticator - Application Runner
Main entry point for running the application
"""

import os
import sys
from flask import Flask
from config import get_config
from database import init_database
import logging


def create_app(config_name=None):
    """Create and configure Flask application"""
    # Import app here to avoid circular imports
    from app import app
    
    # Load configuration
    if config_name:
        os.environ['FLASK_ENV'] = config_name
    
    config = get_config()
    app.config.from_object(config)
    
    # Initialize database
    try:
        db_manager = init_database()
        app.db_manager = db_manager
        print(f"✅ Database initialized: {'MongoDB' if db_manager.is_using_mongodb() else 'SQLite'}")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    
    # Setup logging
    setup_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    return app


def setup_logging(app):
    """Setup application logging"""
    if not app.debug:
        # Production logging
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        file_handler = logging.FileHandler(app.config['LOG_FILE'])
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.info('AI Hadith Authenticator started')


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Page not found', 'success': False}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        return {'error': 'Internal server error', 'success': False}, 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return {'error': 'Access forbidden', 'success': False}, 403
    
    @app.errorhandler(429)
    def rate_limit_error(error):
        return {'error': 'Rate limit exceeded', 'success': False}, 429


def register_cli_commands(app):
    """Register CLI commands"""
    
    @app.cli.command()
    def init_db():
        """Initialize database"""
        from database import init_database
        try:
            db_manager = init_database()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
    
    @app.cli.command()
    def create_admin(email, password, name):
        """Create admin user"""
        from database import DatabaseManager, UserModel
        from utils import hash_password, generate_token
        from datetime import datetime
        
        try:
            db_manager = DatabaseManager()
            user_model = UserModel(db_manager)
            
            # Check if user already exists
            existing_user = user_model.get_user_by_email(email)
            if existing_user:
                print(f"❌ User with email {email} already exists")
                return
            
            # Create admin user
            admin_data = {
                'name': name,
                'email': email,
                'password': password,  # Will be hashed in UserModel
                'created_at': datetime.now().isoformat(),
                'is_verified': True,
                'verification_token': None
            }
            
            user = user_model.create_user(admin_data)
            if user:
                print(f"✅ Admin user created successfully: {email}")
            else:
                print("❌ Failed to create admin user")
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
    
    @app.cli.command()
    def test_db():
        """Test database connection"""
        from database import check_database_health
        
        try:
            health = check_database_health()
            print(f"Database Health: {health}")
        except Exception as e:
            print(f"❌ Database test failed: {e}")
    
    @app.cli.command()
    def cleanup():
        """Cleanup old data"""
        from utils import cleanup_old_files
        from config import get_config
        
        try:
            config = get_config()
            
            # Cleanup old uploads
            deleted_files = cleanup_old_files(config.UPLOAD_FOLDER, 7)
            print(f"✅ Cleaned up {deleted_files} old files")
            
            # Cleanup old cache
            if os.path.exists(config.HF_MODEL_CACHE_DIR):
                deleted_cache = cleanup_old_files(config.HF_MODEL_CACHE_DIR, 1)
                print(f"✅ Cleaned up {deleted_cache} old cache files")
                
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
    
    @app.cli.command()
    def backup():
        """Backup database"""
        from database import backup_database
        
        try:
            backup_database()
            print("✅ Database backup completed")
        except Exception as e:
            print(f"❌ Database backup failed: {e}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Hadith Authenticator')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--config', choices=['development', 'testing', 'production'], 
                       default='development', help='Configuration to use')
    
    args = parser.parse_args()
    
    # Set environment
    if args.config:
        os.environ['FLASK_ENV'] = args.config
    
    if args.debug:
        os.environ['FLASK_DEBUG'] = '1'
    
    # Create app
    app = create_app(args.config)
    
    print(f"""
🕌 AI Hadith Authenticator Starting...
📊 Configuration: {args.config}
🌐 Host: {args.host}
🔌 Port: {args.port}
🐛 Debug: {args.debug}
📅 Started: {app.config.get('START_TIME', 'Unknown')}
    """)
    
    # Run app
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 AI Hadith Authenticator stopped gracefully")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
