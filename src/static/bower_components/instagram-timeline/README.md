# instagram-timeline

It is a [Polymer](https://www.polymer-project.org/1.0/) component for obtain the timeline of the social network Instagram using Polymer

## Use
```html
<instagram-timeline access-token="<your_token>" endpoint="<your_endpoint>" language=[<your_endpoint>]></instagram-timeline>
```
## Properties

|                     | Properties                                                                                                                                   |                                   |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| endpoint            | The URL where you must make a instagram requests. You must provide one.                                                                                       | Required  `<String>`                |
| access-token               | The access_token to get the user's instagram                                                                   | Required `<String>`               |
| component_directory | The component directory where the component is. You must provide it when your component directory is different that your project directory. | Optional `<String>`               |
| count            | The number of pictures per request.                                                                                                           | Optional Default: 15  `<Integer>` |
| language            | The language in which you want to get the pictures (only allow `en` (english) and `es` (spanish) at the moment)                                | Optional Default: es `<String>`   |
| refresh_time            | How often the component refreshes the pictures (milliseconds)                              | Optional Default: `60000` `<Integer>`   |

## Parser Status

- [x] Date
- [x] Hashtag
- [x] Url
- [x] Username
- [x] Mentions
- [x] Likes
- [ ] Comments
- [ ] Like a picture
