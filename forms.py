from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp
import re

class SQLInjectionValidator:
    """Custom validator to prevent SQL injection attempts"""
    def __init__(self, message=None):
        if not message:
            message = 'Input contains potentially dangerous characters'
        self.message = message

    def __call__(self, form, field):
        # List of common SQL injection keywords and patterns
        sql_keywords = [
            'select', 'insert', 'update', 'delete', 'drop', 'create', 'alter',
            'union', 'script', 'exec', 'execute', 'sp_', 'xp_', '--', ';',
            'or 1=1', 'or 1 = 1', 'and 1=1', 'and 1 = 1', '<script', '</script>'
        ]
        
        input_lower = field.data.lower() if field.data else ''
        
        # Check for SQL injection patterns
        for keyword in sql_keywords:
            if keyword in input_lower:
                raise ValueError(f'Potentially dangerous input detected: {keyword}')
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r"['\";]",  # Quotes and semicolons
            r"--",      # SQL comments
            r"/\*.*\*/", # SQL block comments
            r"<script.*?>.*?</script>", # Script tags
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, input_lower, re.IGNORECASE):
                raise ValueError('Input contains potentially dangerous characters')

class UserForm(FlaskForm):
    fname = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters'),
        Regexp(r'^[A-Za-z\s\-\']+$', message='First name can only contain letters, spaces, hyphens, and apostrophes'),
        SQLInjectionValidator()
    ])
    
    lname = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters'),
        Regexp(r'^[A-Za-z\s\-\']+$', message='Last name can only contain letters, spaces, hyphens, and apostrophes'),
        SQLInjectionValidator()
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=200, message='Email must be less than 200 characters'),
        SQLInjectionValidator()
    ])
    
    submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    fname = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters'),
        Regexp(r'^[A-Za-z\s\-\']+$', message='First name can only contain letters, spaces, hyphens, and apostrophes'),
        SQLInjectionValidator()
    ])
    
    lname = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters'),
        Regexp(r'^[A-Za-z\s\-\']+$', message='Last name can only contain letters, spaces, hyphens, and apostrophes'),
        SQLInjectionValidator()
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=200, message='Email must be less than 200 characters'),
        SQLInjectionValidator()
    ])
    
    submit = SubmitField('Update')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=4, max=20, message='Username must be between 4 and 20 characters'),
        Regexp(r'^[A-Za-z0-9_]+$', message='Username can only contain letters, numbers, and underscores'),
        SQLInjectionValidator()
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters'),
        SQLInjectionValidator()
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, max=128, message='Password must be between 8 and 128 characters'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]', 
               message='Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character')
    ])
    
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        SQLInjectionValidator()
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    
    submit = SubmitField('Login')