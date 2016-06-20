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
| refresh_time            | how often the component refresh the data (milliseconds)                                                                                                           | Optional Default: 60000  `<Integer>`  |
| language            | The language in which you want to get the posts (only allow `en` (english) and `es` (spanish) at the moment)                                | Optional Default: es `<String>`   |

## Parser Status

- [x] 1.PushEvent
- [x] 2.WatchEvent
- [x] 3.CreateEvent
- [x] 4.PullRequestEvent
- [x] 5.IssuesEvent
  - [x] opened
  - [x] closed
  - [x] reopened
  - [ ] assigned (useless)
  - [ ] unassigned (useless)
  - [ ] labeled (useless)
  - [ ] unlabeled (useless)
- [x] 6.MemberEvent
- [X] 7.ReleaseEvent
- [X] 8.CommitCommentEvent
- [x] 9.DeleteEvent
- [x] 10.GollumEvent*
- [X] 11.IssueCommentEvent
- [ ] 12.PublicEvent
- [ ] 13.PullRequestReviewCommentEvent
- [X] 14.ForkEvent
- [ ] 15.TeamAddEvent
- [ ] 16.StatusEvent
- [ ] 17.RepositoryEvent
- [ ] 18.PageBuildEvent
- [ ] 19.MembershipEvent
- [ ] 20.GistEvent
- [ ] 21.ForkApplyEvent
- [ ] 22.FollowEvent
- [ ] 23.DownloadEvent
- [ ] 24.DeploymentStatusEvent
- [ ] 25.DeploymentEvent

* No testing yet
