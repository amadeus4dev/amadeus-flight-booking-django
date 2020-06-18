# Amadeus Flight Booking

We recently released our first booking API to give you the chance to integrate booking capabilities directly in your application. In this prototype we demonstrate the end-to-end booking process, which works in conjunction with three APIs:
* [Flight Offer Search](https://developers.amadeus.com/self-service/category/air/api-doc/flight-offers-search): to search for the best bookable flight offers.
* [Flight Offer Price](https://developers.amadeus.com/self-service/category/air/api-doc/flight-offers-price):  confirms the latest price and availability of a specific chosen flight.
* [Flight Create Orders](https://developers.amadeus.com/self-service/category/air/api-doc/flight-create-orders): to book flights and ancillary services proposed by the airline.

The [application](https://amadeus4dev-book-flight.herokuapp.com) is also hosted, so you can play directly with it. 

## How to run the project via Docker (recommended)

Build the image from the Dockerfile. The following command will 

```sh
make
```

The container receives your API key/secret from the environment variables.
Before running the container, make sure your have your credentials correctly
set:

```sh
export AMADEUS_CLIENT_ID=YOUR_API_KEY
export AMADEUS_CLIENT_SECRET=YOUR_API_SECRET
```

Finally, start the container from the image:

```
make run
```

At this point you can open a browser and go to `https://0.0.0.0:8000`.

Note that it is also possible to run in detached mode so your terminal is still
usable:

```
make start
```

Stop the container with:

```
make stop
```

## How to run the project locally

Clone the repository.

```sh
git clone https://github.com/amadeus4dev/amadeus-flight-booking-django.git
cd amadeus-flight-booking-django
```

Next create a virtual environment with [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html) and install the dependencies.

```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Windows run the command below to activate the virtual environment.
``` 
./venv/scripts/activate.bat
```

For authentication add your API key/secret to your `.bashrc` or `.zshrc` files.

```sh
export AMADEUS_CLIENT_ID=YOUR_API_KEY
export AMADEUS_CLIENT_SECRET=YOUR_API_SECRET
```

You can easily switch between `test` and `production` environments by setting:

```
export AMADEUS_HOSTNAME="test" # an empty value will also set the environment to test
```

or

```
export AMADEUS_HOSTNAME="production"
```

> Each environment has different API keys. Do not forget to update them!

Finally, run the Django server.

```sh
python amadeus_demo_api/manage.py runserver
```

Finally, open a browser and go to `https://127.0.0.1:8000`

## License

This library is released under the [MIT License](LICENSE).

## Help

Our [developer support team](https://developers.amadeus.com/support) is here
to help you. You can find us on
[StackOverflow](https://stackoverflow.com/questions/tagged/amadeus) and
[email](mailto:developers@amadeus.com).
