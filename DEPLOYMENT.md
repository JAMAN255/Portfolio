# Deployment Configuration Guide

## Railway.app Deployment Setup

This project is configured for deployment on Railway.app using `railpack.json`.

### Environment Variables Required

Before deploying, set these environment variables in your Railway project:

1. **SECRET_KEY** - Generate a secure secret key for production
   ```
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **DATABASE_URL** - PostgreSQL connection string (auto-provided by Railway if enabled)
   - Format: `postgresql://user:password@host:port/dbname`

3. **REDIS_URL** - Redis connection string (auto-provided by Railway if enabled)
   - Format: `redis://user:password@host:port`

4. **ALLOWED_HOSTS** - Add your Railway domain
   - Format: `yourdomain.railway.app,yourdomain.com`

5. **DEBUG** - Set to `False` for production

### Deployment Steps

1. Connect your GitLab/GitHub repository to Railway
2. Configure environment variables in Railway dashboard
3. Enable PostgreSQL and Redis plugins in Railway
4. Deploy via push to your repository's main branch

### Services Included

- **web**: Main Gunicorn WSGI server (1 replica by default)
- **worker**: Celery background task worker (0 replicas by default - enable if needed)
- **beat**: Celery scheduler (0 replicas by default - enable if needed)
- **postgres**: PostgreSQL database (version 15)
- **redis**: Redis cache/message broker (version 7)

### Post-Deployment

After initial deployment, run migrations:

```bash
railway run python myapp/manage.py migrate
```

Create a superuser (optional):

```bash
railway run python myapp/manage.py createsuperuser
```

### Production Checklist

- [ ] Set SECRET_KEY to a random secure value
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Update DATABASE_URL for PostgreSQL
- [ ] Configure REDIS_URL for caching and Celery
- [ ] Run migrations on production database
- [ ] Collect static files (handled in Dockerfile)
- [ ] Test email configuration (if applicable)
- [ ] Set up logging and monitoring
- [ ] Enable HTTPS/SSL certificate

### Static Files & Media

Static files are collected during Docker build and served by your web server.
Media files are stored in the `media/` volume for persistence.

### Scaling

To enable Celery workers or beat scheduler:
1. Set `numReplicas` in railpack.json for `worker` and `beat` processes
2. Push changes to trigger redeployment

### Troubleshooting

Check Railway logs:
```bash
railway logs
```

SSH into running container:
```bash
railway shell
```

Run management commands:
```bash
railway run python myapp/manage.py <command>
```
