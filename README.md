# AI Hadith Authenticator

A comprehensive web application for authenticating Islamic hadith using AI technology.

## Features

- **AI-Powered Authentication**: Uses advanced machine learning models to analyze hadith authenticity
- **Multi-Modal Input**: Support for text, image, and audio analysis
- **Real-Time Search**: Search through authentic hadith collections
- **Quran Reader**: Interactive Quran browsing with multiple translations
- **User Authentication**: Secure user registration and login system
- **Professional UI**: Modern glass morphism design with responsive layout
- **Database Fallback**: MongoDB with SQLite fallback for reliability

## Technology Stack

### Backend
- **Flask**: Python web framework
- **MongoDB**: Primary database with SQLite fallback
- **Hugging Face**: AI model integration
- **Transformers**: Direct model loading capability
- **PyTorch**: Deep learning framework
- **Flask-Bcrypt**: Password hashing
- **Flask-Mail**: Email functionality

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript**: Interactive functionality
- **Glass Morphism**: Professional UI design

### AI/ML
- **Hugging Face Spaces**: Cloud-based model inference
- **Direct Model Import**: Local model loading capability
- **Transformers Library**: State-of-the-art NLP models
- **Multi-Tier Fallback**: Direct model → HF API → Keyword analysis

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-hadith-authenticator
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Create .env file
   HF_TOKEN=your_huggingface_token
   MONGODB_URI=mongodb://localhost:27017/hadith_auth
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   GEMINI_API_KEY=your_gemini_key
   SECRET_KEY=your_secret_key
   SUNNAH_API_KEY=your_sunnah_key
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

## Project Structure

```
ai-hadith-authenticator/
├── app.py                     # Main Flask application
├── direct_model_import.py       # Direct model loading utility
├── requirements.txt            # Python dependencies
├── .env                      # Environment variables
├── templates/                 # HTML templates
│   ├── index.html            # Main dashboard
│   ├── hadith_analyzer.html  # Hadith analysis interface
│   ├── login.html           # User login
│   ├── signup.html          # User registration
│   └── quran.html          # Quran reader
├── static/                   # Static assets
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Image assets
├── venv/                    # Virtual environment
├── users.db                 # SQLite fallback database
└── README.md                # This file
```

## API Endpoints

### Authentication
- `POST /signup` - User registration
- `POST /login` - User login
- `POST /logout` - User logout

### Main Features
- `GET /` - Main dashboard
- `GET /hadith-analyzer` - Hadith analysis interface
- `POST /analyze-hadith` - Analyze hadith text/media
- `GET /search` - Search hadith database
- `GET /quran` - Quran reader interface
- `POST /chat` - AI chat assistant

### External APIs
- **Hugging Face Spaces**: AI model inference
- **Sunnah.com**: Hadith verification
- **Gemini AI**: Chat assistance

## Model Information

The application uses the AI Hadith Authentication model:
- **Repository**: `abbasorakzai777/ai-hadith-authentication`
- **Model Path**: `final_model`
- **Classes**: Sahih, Hasan, Da'if, Mawdu', Not classified
- **Input Types**: Text, Image, Audio
- **Output**: Grade, Confidence, Warning, Isnad, Source

## Configuration

### Environment Variables
- `HF_TOKEN`: Hugging Face authentication token
- `MONGODB_URI`: MongoDB connection string
- `MAIL_USERNAME`: Email for notifications
- `MAIL_PASSWORD`: Email app password
- `GEMINI_API_KEY`: Google Gemini API key
- `SECRET_KEY`: Flask secret key
- `SUNNAH_API_KEY`: Sunnah.com API key

### Model Settings
- `HF_SPACE_ID`: Hugging Face space ID
- `HF_MODEL_SUBDIR`: Model subdirectory (final_model)
- `HF_MODEL_CACHE_DIR`: Local cache directory

## Features in Detail

### Hadith Analysis
1. **Direct Model Loading**: Local model inference for speed
2. **Hugging Face API**: Cloud-based analysis
3. **Intelligent Fallback**: Keyword-based analysis
4. **Multi-Modal Support**: Text, image, audio input
5. **Confidence Scoring**: AI confidence percentages
6. **Chain Verification**: Isnad analysis
7. **Source Attribution**: Source identification

### Search Engine
1. **Real Database**: Authentic hadith collections
2. **Full-Text Search**: English and Arabic content
3. **Source Verification**: Authentic source checking
4. **Grade Display**: Authenticity grades
5. **Fast Results**: Optimized search performance

### Quran Reader
1. **Surah Navigation**: All 114 surahs
2. **Verse Display**: Arabic with translations
3. **Multiple Languages**: English translations
4. **Responsive Design**: Mobile-friendly interface
5. **Bookmark Support**: Save favorite verses

## Security Features

### Authentication
- **Password Hashing**: bcrypt encryption
- **Session Management**: Secure sessions
- **Email Verification**: User verification
- **MongoDB Integration**: Secure database
- **SQLite Fallback**: Data persistence

### Data Protection
- **Input Validation**: Form validation
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Output sanitization
- **CSRF Protection**: Flask security
- **HTTPS Ready**: SSL configuration

## Performance

### Optimization
- **Model Caching**: Reduce API calls
- **Database Indexing**: Fast queries
- **Static Caching**: Asset optimization
- **Lazy Loading**: On-demand content
- **Compression**: Gzip support

### Monitoring
- **Error Logging**: Comprehensive logging
- **Performance Metrics**: Response times
- **User Analytics**: Usage tracking
- **Model Performance**: Accuracy monitoring
- **System Health**: Status monitoring

## Deployment

### Production
1. **Environment Setup**: Production variables
2. **Database Setup**: MongoDB cluster
3. **Web Server**: Gunicorn/Nginx
4. **SSL Certificate**: HTTPS setup
5. **Domain Configuration**: DNS settings
6. **Monitoring**: Application monitoring

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## Troubleshooting

### Common Issues
1. **Model Loading**: Check HF_TOKEN and internet
2. **Database Connection**: Verify MONGODB_URI
3. **Email Issues**: Check MAIL settings
4. **Performance**: Monitor memory usage
5. **Dependencies**: Ensure all packages installed

### Debug Mode
```bash
export FLASK_DEBUG=1
python app.py
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review troubleshooting guide

---

**AI Hadith Authenticator** - Combining traditional Islamic knowledge with modern AI technology for authentic hadith verification.
