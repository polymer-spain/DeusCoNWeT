# github-events

It is a [Polymer](https://www.polymer-project.org/1.0/) component that show Github events from a user's account.

## Use
`<github-events username="<username>"></github-events>`

## Properties

|                     | Properties                                                                                                                                   |                                   |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| username            | The username on Github that you want to get her events                                                                                      | Required  `<String>`                |
| token               | The access_token on Github. If you use it, you have more request per hour                                                                   | Optional `<String>`               |
| component_directory | The component directory where the component is. You must provide it when your component directory is different that your project directory. | Optional `<String>`               |
| per_page            | The number of events per request.                                                                                                           | Optional Default: 15  `<Integer>` |
| language            | The language in which you want to get the posts (only allow `en` (english) and `es` (spanish) at the moment)                                | Optional Default: es `<String>`   |

## Parser Status

- [x] PushEvent
- [x] WatchEvent
- [x] CreateEvent
- [x] PullRequestEvent
- [ ] IssuesEvent
- [ ] MemberEvent
- [ ] ReleaseEvent
- [ ] CommitCommentEvent
- [ ] DelateEvent
- [ ] GollumEvent
- [ ] IssueCommentEvent
- [ ] PublicEvent
- [ ] PullRequestReviewCommentEvent
