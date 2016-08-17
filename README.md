# SKUGen

**A Django-driven product organization app for designing product inventory
and stock keeping units (SKUs).** You can then export the data structure out
for importing into systems such as [Shopify](http://www.shopify.com) and
[Magento](http://www.magento.com).

## Setup

If you have Docker and Docker Compose installed, installation should be as simple
as cloning the repo and then ```docker-compose up```.

## Detailed Setup Instructions

### Step 1: Clone and Build

```
$ git clone https://github.com/MarconiMediaGroup/SKUGen.git
$ cd SKUGen
$ docker-compose build
```
Wait for a bit while the image layers download.


### Step 2: Bring Up the DB Image

```
$ docker-compose up -d db ; docker-compose logs -f
```
I recommend bringing the database up first. Even though it's been set as a
dependency for Web, the timing still isn't quite right -- so the web app
can start running and fail trying to access the database. (If you have
suggestions on how to better handle this, do let me know... or even better,
submit a PR with the fix).

Once you see it is up and running (something like ```db_1   | LOG:  autovacuum
launcher started``` appears on screen, you can safely hit CTRL-C to proceed.


### Step 3: Bring Up the Web Image

```
$ docker-compose up -d web ; docker-compose logs -f
```

Give it a second and you should see something like:

```
web_1  |  * Running on http://0.0.0.0:8010/ (Press CTRL+C to quit)
web_1  |  * Restarting with stat
web_1  | Performing system checks...
web_1  |
web_1  | System check identified no issues (0 silenced).
web_1  |
web_1  | You have unapplied migrations; your app may not work properly until they are applied.
web_1  | Run 'python manage.py migrate' to apply them.
web_1  |
web_1  | Django version 1.9.9, using settings 'project.settings'
web_1  | Development server is running at http://0.0.0.0:8010/
web_1  | Using the Werkzeug debugger (http://werkzeug.pocoo.org/)
web_1  | Quit the server with CONTROL-C.
web_1  |  * Debugger is active!
web_1  |  * Debugger pin code: 521-558-709
```

### Step 4: Schema and Admin

Now your Web image is running, so you can perform the initial data schema
migration and create your admin user:

```
$ docker-compose run --rm web python manage.py migrate
$ docker-compose run --rm web python manage.py createsuperuser
```

You'll be prompted for a username, email address and password. Provide those,
and you should be ready to go.

### Step 5: Open a Browser and Start Work

The admin site should now be available here: ```http://127.0.0.1:8010/admin```.


## Problems & Troubleshooting

If you run into any problems,  [open an issue](https://github.com/MarconiMediaGroup/SKUGen/issues/new).
