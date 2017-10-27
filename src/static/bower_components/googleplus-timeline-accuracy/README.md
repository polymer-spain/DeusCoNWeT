# googleplus-timeline

[Polymer](https://www.polymer-project.org/1.0/) Web Component that obtains Google+ feed for an user.

**Note**: This version adds accuracy defects (changes author of the post to a generic identifier) for final-user testing research purposes. The probability of these accuracy defects can be setted with the "accuracy-probability" param.
## Use
```html
    <googleplus-timeline token="USER_ACCESS_TOKEN"> </googleplus-timeline>
```

## Properties

|                     | Properties                                                                                                                                   |                                   |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| token               | Google+ access token of the logged in user                                                                   | Required `<String>`               |
| language               | Language of information provided by the component (details about a certain post, not the post content itself)                                                                   | Optional `<String>`  (Default: 'en')             |
| accuracy-probability               | Sets the probability to introduce accuracy defects to the information displayed by the component  | Optional `<Integer>` (Default: 15)              |

## Dependencies

Element dependencies are managed via [Bower](http://bower.io/). You can
install that via:

    npm install -g bower

Then, go ahead and download the element's dependencies:

    bower install
