'use strict';

const e = React.createElement;

const SumbissionMediaType = {
  text: 1,
  image: 2,
  video: 3
};

function format_upvotes(upvotes) {
  if (upvotes >= 1000) {
    return Math.floor(upvotes / 1000) + "k";
  } else {
    return upvotes
  }
}

class RedditFeed extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      submissions: [],
      finished_loading: false,
      sort: "rating",
      skip: null,
      subreddits: [],
      subreddits_expand: false
    };
  }

  async componentDidMount() {
    while (this.state.finished_loading == false && this.state.error == null) {
      if (this.state.skip == null)
        this.state.skip = 0;
      else
        this.state.skip += 10;
      try {
        const response = await fetch("/api/reddit-feed/?skip=" + this.state.skip);
        const res = await response.json();
        let current_submissions = this.state.submissions;
        let current_subreddits = this.state.subreddits;

        if (res.length == 0) {
          this.setState({finished_loading: true})
        }
        else {
          for (let i=0; i < res.length; i++) {
            let submission = res[i];
            submission.show = true;
            submission.show_comments = false;
            if (submission.media_type == SumbissionMediaType.video) {
              submission.media_html = <video controls src={submission.url}></video>;
            } else if (submission.media_type == SumbissionMediaType.image) {
              submission.media_html = <img src={submission.url}/>;
            } else {
              submission.media_html = <a href={submission.url}>Source</a>;
            }
            if (current_subreddits.find((subreddit) => subreddit.name === submission.subreddit) == undefined)
              current_subreddits.push({name: submission.subreddit, show: true});
          }

          current_submissions.push(...res);
          this.setState({ 
            submissions: current_submissions,
            subreddits: current_subreddits
          });
        }
      } catch (error) {
        this.setState({
          error: error
        })
      }
    }
  }

  update_sorting = (e) => {
    var submissions = this.state.submissions;

    if (e.target.value == "rating") {
      submissions.sort((a,b) => b.rating - a.rating);
    }
    else if (e.target.value == "upvotes") {
      submissions.sort((a,b) => b.upvotes - a.upvotes);
    }
    this.setState({
      submissions: submissions,
      sort: e.target.value     
    });
  }


  toggle_comments = (index) => {
    var submissions = this.state.submissions;
    submissions[index].show_comments = !submissions[index].show_comments;
    this.setState({
      submissions: submissions
    });
  }

  show_checkboxes = (e) => {
    e.preventDefault();
    let expanded = this.state.subreddits_expand;
    var checkboxes = document.getElementById("checkboxes");
    if (!expanded) {
      checkboxes.style.display = "block";
      expanded = true;
    } else {
      checkboxes.style.display = "none";
      expanded = false;
    }
    this.setState({subreddits_expand: expanded})
  }

  toggle_subreddit = (index) => {
    index = index.index;
    var subreddits = this.state.subreddits;
    subreddits[index].show = !subreddits[index].show;

    var submissions = this.state.submissions;
    for (let i=0; i<submissions.length; i++)
      if (submissions[i].subreddit == subreddits[index].name) {
        submissions[i].show = subreddits[index].show;
        console.log(submissions[i]);
      }

    this.setState({
      subreddits: subreddits,
      submissions: submissions
    })
  }

  render() {
    const { error, submissions, sort, finished_loading, skip, subreddits } = this.state;
    if (error) {
      return ({error})
    }
    else {
      return (
          <div>
            <div className="reddit-feed-settings">
              <select onChange={this.update_sorting}>
                <option value="rating">Sort by rating</option>
                <option value="upvotes">Sort by upvotes</option>
                {/*<option value="random">Sort by random</option>*/}
              </select>
              <div className="multiselect">
                <div className="selectBox" onClick={this.show_checkboxes}>
                  <select onMouseDown={(e) => e.preventDefault()}>
                    <option>Subreddits</option>
                    <div className="overSelect"></div>
                  </select>
                </div>
                <div id="checkboxes">
                  {subreddits.map((subreddit, index) => {
                    return (
                      <label for={index.toString()}><input type="checkbox" onChange={() => this.toggle_subreddit({index})} 
                      checked={subreddit.show} id={index.toString()} />{subreddit.name}</label>
                      )
                  })}
                  </div>
                </div>
            </div>
            <div className="reddit-feed-submissions">
            { submissions.map((submission, index) => {
                if (submission.show)
                  return (
                    <div className="submission" key={index.toString()}>
                      <hr></hr>
                      <div className="title">
                        <h2>{submission.title}</h2>
                        {sort == "rating" ? <span>{format_upvotes(submission.rating)}</span> : <span>{format_upvotes(submission.upvotes)}</span>}
                      </div>
                      <p>{submission.text}</p>
                      <div>{submission.media_html}</div>
                      <div className="comments">
                        <button onClick={() => this.toggle_comments(index)}>Comments</button>
                        { submission.show_comments ? 
                            submission.comments.filter((comment) => comment.parent_id == null).map((comment, index) => {
                              if (!comment.author.includes("Bot") && !comment.author.includes("Moderator"))
                                return (
                                  <div className="comment" key={index.toString()}>
                                    <p className="author">u/{comment.author}</p>
                                    <div className="body">
                                      <p dangerouslySetInnerHTML={{__html: comment.body}}></p>
                                      {sort == "rating" ? <span>{format_upvotes(comment.rating)}</span> : <span>{format_upvotes(comment.upvotes)}</span>}
                                    </div>
                                    <p>----</p>
                                    { submission.comments.filter((reply) => reply.parent_id == comment.id).map((reply, index) => {
                                      return (
                                        <div className="reply" key={index.toString()}>
                                          <p className="author">u/{reply.author}</p>
                                          <div className="body">
                                            <p dangerouslySetInnerHTML={{__html: reply.body}}></p>
                                            {sort == "rating" ? <span>{format_upvotes(reply.rating)}</span> : <span>{format_upvotes(reply.upvotes)}</span>}
                                          </div>
                                          <p>--</p>
                                        </div>
                                      )
                                    }) }
                                  </div>
                                  )
                          }) : null }
                      </div>
                    </div>
                  )
            })}
            </div>
          </div>
        )
    }
  }
}

const domContainer = document.querySelector('#reddit_feed');
const root = ReactDOM.createRoot(domContainer);
root.render(e(RedditFeed));