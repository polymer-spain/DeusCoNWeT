# Facebook wall

It is a [Polymer](https://www.polymer-project.org/1.0/) component which show a Facebook wall.

`<facebook-wall>`

The `facebook-wall` element displays a Facebook wall.
For use it, you  must take an `access token` of the user that you want to show him facebook's wall.

**NOTE**: you need a [`read_stream`](https://developers.facebook.com/docs/facebook-login/permissions/v2.3) permission to
getting user's posts. Now I use mocked data.

## Example

```html
  <facebook-wall access_token="\<your_access_token\>" language="en"></facebook-wall>
```

## To get Access Token

You can get an access token using the [`login-facebook`](https://github.com/Mortega5/login-facebook) component or
using [Facebook API](https://developers.facebook.com/docs/facebook-login/access-tokens)


## Status

+ [ ] Parse status?


  |                      | link | video | photo | status | offer | post |
  |----------------------|:------:|:------:|:-------:|:--------:|:-------:|:-------:|
  | mobile_status_update |      |      |       |        |       |       |
  | created_note         |      |      |       |        |       |       |
  | added_photos         |      |      |       |        |       |       |
  | added_video          |      |      |       |        |       |       |
  | shared_story         |:white_check_mark:|:white_check_mark:|:white_check_mark:|        |       |       |
  | created_group        |      |      |       |        |       |       |
  | created_event        |      |      |       |        |       |       |
  | wall_post            |      |      |       |        |       |       |
  | app_created_story    |      |      |       |        |       |       |
  | published_story      |      |      |       |        |       |       |
  | tagged_in_photo      |      |      |       |        |       |       |
  | approved_friend      |      |      |       |        |       |       |


+ [ ] `Likes` only return 25 post, I cannot get *#likes* with this field. Use GET to `/{object_id}/likes?summary=true`
      The response have *#likes*.

+ [x] Wrap post with border. Which ones?.

+ [x] Some linked posts have `story` field, some need use it as "general header".

+ [ ] Add `name` and `message` format to `shared_story` and `type link`.

+ [x] Get Post with correct language. (use the correct request)

+ [ ] Refresh post messages when the language change.

+ [x] Use API to get user's posts. (you need `read_stream` permissions)







