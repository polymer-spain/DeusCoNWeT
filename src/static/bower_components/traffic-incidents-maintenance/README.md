# traffic-incidents
[Documentation and demo](https://mortega5.github.io/traffic-incidents)

Show a timeline of traffic issues. Its use two api:

- **Google Maps Geocoding API**: to convert any address to geographical coordinates.

- **Bing Maps Traffic API**    : to get information about traffic issues in any city.

Example:

```html
<traffic-incidents city="Madrid" api_key_geocoding="your_google_geocoding_key"
app_key_traffic="yout_bing_maps_key" auto_refresh refresh_time="60000">
```

**NOTE** : Bing Maps API provide the traffic incident text in the primary language of the country
where the incident occurs. For more information go to : https://msdn.microsoft.com/en-us/library/jj136866.aspx

## Dependencies

Element dependencies are managed via [Bower](http://bower.io/). You can
install that via:

    npm install -g bower

Then, go ahead and download the element's dependencies:

    bower install


## Playing With Your Element

If you wish to work on your element in isolation, we recommend that you use
[Polyserve](https://github.com/PolymerLabs/polyserve) to keep your element's
bower dependencies in line. You can install it via:

    npm install -g polyserve

And you can run it via:

    polyserve

Once running, you can preview your element at
`http://localhost:8080/components/traffic-incidents/`, where `traffic-incidents` is the name of the directory containing it.


## Testing Your Element

Simply navigate to the `/test` directory of your element to run its tests. If
you are using Polyserve: `http://localhost:8080/components/traffic-incidents/test/`

### web-component-tester

The tests are compatible with [web-component-tester](https://github.com/Polymer/web-component-tester).
Install it via:

    npm install -g web-component-tester

Then, you can run your tests on _all_ of your local browsers via:

    wct

#### WCT Tips

`wct -l chrome` will only run tests in chrome.

`wct -p` will keep the browsers alive after test runs (refresh to re-run).

`wct test/some-file.html` will test only the files you specify.


## Yeoman support

If you'd like to use Yeoman to scaffold your element that's possible. The official [`generator-polymer`](https://github.com/yeoman/generator-polymer) generator has a [`seed`](https://github.com/yeoman/generator-polymer#seed) subgenerator.
