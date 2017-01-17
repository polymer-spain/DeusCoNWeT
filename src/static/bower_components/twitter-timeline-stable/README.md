# twitter-timeline

It is a [Polymer](https://www.polymer-project.org/1.0/) component for obtain the timeline of Twitter.

## Use
`<twitter-timeline username="<username>"></twitter-timeline>`

## Properties

|                     | Properties                                                                                                                                   |                                   |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| endpoint            | Url where the backend handle the twitter request. You must create one for that.                                                                                      | Required  `<String>`                |
| access_token               | The access_token on Github. If you use it, you have more request per hour                                                                   | Optional `<String>`               |
| component_directory | The component directory where the component is. You must provide it when your component directory is different that your project directory. It is must end with `/`| Optional Default: ./  `<String>`               |
| count            | The number of tweets per request.                                                                                                           | Optional Default: 200  `<Integer>` |
| language            | The language in which you want to get the tweets (only allow `en` (english) and `es` (spanish) at the moment)                                | Optional Default: es `<String>`   |


