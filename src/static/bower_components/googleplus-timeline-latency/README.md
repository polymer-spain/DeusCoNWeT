# googleplus-timeline

[Polymer](https://www.polymer-project.org/1.0/) Web Component that obtains Google+ feed for an user.

**Note**: This version adds latency defects (slower reactions to user interactions) for final-user testing research purposes. The latency can be setted with the "latency-time" param.

## Use
```html
    <googleplus-timeline token="USER_ACCESS_TOKEN"> </googleplus-timeline>
```

## Properties

|                     | Properties                                                                                                                                   |                                   |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| token               | Google+ access token of the logged in user                                                                   | Required `<String>`               |
| language               | Language of information provided by the component (details about a certain post, not the post content itself)                                                                   | Optional `<String>`    (Default: 'en')           |
| latency-time               | Latency (in milliseconds) intended to be introduced to the component.behaviour                                                                   | Optional `<Integer>`    (Default: 2000 milliseconds)           |

## Obtaining an access token
When you complete the G+ sign in flow, you obtain an access token necessary to authenticate you through the subsecuent calls to the Google+ API. This component needs it to obtain info (posts) on user's behalf.  To implement/integrate the sign in flow in your application/site please visit [Sign In Users](https://developers.google.com/+/web/signin/) and [Integrating Google Sign-In into your web app](https://developers.google.com/identity/sign-in/web/sign-in). You can find [here](https://developers.google.com/identity/) some examples also.

## Dependencies

Element dependencies are managed via [Bower](http://bower.io/). You can
install that via:

    npm install -g bower

Then, go ahead and download the element's dependencies:

    bower install
