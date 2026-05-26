# Deployment Configuration Guide

## Railway.app Deployment Setup

This project is configured for deployment on Railway.app using `railpack.json`.

### Key Configuration Changes

- Uses **Gunicorn** (production WSGI server) instead of `manage.py runserver`
- Automatically runs migrations on startup
- Uses **WhiteNoise** for optimized static file serving
- Supports PostgreSQL when `DATABASE_URL` environment variable is set
- Falls back to SQLite for development

### Environment Variables Required

Before deploying, set these environment variables in your Railway project:

1. **SECRET_KEY** - Generate a secure secret key for production
   ```
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **DATABASE_URL** - PostgreSQL connection string (auto-provided by Railway if enabled)
   - Format: `postgresql://user:password@host:port/dbname`
   - Railway provides this automatically when you enable the PostgreSQL plugin

3. **REDIS_URL** - Redis connection string (auto-provided by Railway if enabled)
   - Format: `redis://user:password@host:port`
   - Railway provides this automatically when you enable the Redis plugin

4. **ALLOWED_HOSTS** - Add your Railway domain
   - Format: `yourdomain.railway.app,yourdomain.com`
   - Default: `*` (accepts all hosts - update this in production!)

5. **DEBUG** - Set to `False` for production (already default)

### Deployment Steps

1. **Connect your GitLab/GitHub repository to Railway**
   - Go to Railway.app dashboard
   - Click "New Project"
   - Select "Deploy from GitHub/GitLab"

2. **Add Environment Variables**
   - Go to project settings
   - Add `SECRET_KEY` (generate a new one)
   - Add `ALLOWED_HOSTS` with your domain
   - Other variables will be auto-configured by Railway plugins

3. **Enable Database & Cache Add-ons**
   - Click "Add Plugin" in Railway dashboard
   - Add PostgreSQL (version 15)
   - Add Redis (version 7)

4. **Deploy**
   - Push to your main branch - Railway will deploy automatically
   - Or click "Deploy" in Railway dashboard

### Services Included

- **web** (Port 8000): Main Gunicorn WSGI server (1 replica)
- **worker**: Celery background tasks (0 by default - enable if needed)
- **beat**: Celery scheduler (0 by default - enable if needed)
- **postgres**: PostgreSQL database (auto-configured)
- **redis**: Redis cache/broker (auto-configured)

### Post-Deployment

After initial deployment, the migrations run automatically. You may need to:

1. **Create a superuser** (optional for admin access):
   ```bash
   railway run python manage.py createsuperuser
   ```

2. **Check logs** for any errors:
   ```bash
   railway logs
   ```

### Production Checklist

- [x] Uses Gunicorn (production server)
- [x] Migrations run automatically on startup
- [x] Static files collected and compressed
- [x] WhiteNoise middleware configured
- [ ] Set SECRET_KEY to a random secure value
- [ ] Set ALLOWED_HOSTS with your actual domain
- [ ] Enable PostgreSQL and Redis plugins
- [ ] Test email configuration (if applicable)
- [ ] Set up monitoring and error tracking

### Static Files & Media

- **Static files** are collected during Docker build and served by WhiteNoise
- **Media files** are stored in the `media/` directory (persists across deployments)
- No need for a separate web server (Nginx/Apache) - Gunicorn + WhiteNoise handles it

### Scaling

To enable Celery workers or beat scheduler:

1. Edit `railpack.json`
2. Change `"numReplicas": 0` to `"numReplicas": 1` for worker/beat
3. Push changes to trigger redeployment

### Troubleshooting

**Port binding error**
- Make sure the startCommand binds to `0.0.0.0:8000`
- Railway automatically maps port 8000 to the public URL

**Database connection error**
- Ensure DATABASE_URL is set in Railway environment variables
- Check that PostgreSQL plugin is enabled and running
- Run `railway run python manage.py migrate` to verify migrations

**Static files not loading**
- Check that WhiteNoise middleware is in MIDDLEWARE list
- Run `railway run python manage.py collectstatic --noinput`
- Clear browser cache

**Module not found error**
- Verify settings import: `from decouple import config` and `import dj_database_url`
- Check that `requirements.txt` includes: `dj-database-url` and `whitenoise`

**Check Railway logs**:
```bash
railway logs
```

**SSH into container**:
```bash
railway shell
```

**Run management commands**:
```bash
railway run python manage.py <command>
```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'decouple'` | Install dependencies: `pip install -r requirements.txt` |
| `Import error: dj_database_url` | Add `dj-database-url==2.0.0` to requirements.txt |
| `Import error: whitenoise` | Add `whitenoise==6.5.0` to requirements.txt |
| Port already in use | Railway automatically manages ports, shouldn't happen |
| Database migrations not running | Check Dockerfile CMD - migrations run automatically on startup |
