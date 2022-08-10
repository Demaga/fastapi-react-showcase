'use strict';

const e = React.createElement;

const SumbissionMediaType = {
  text: 1,
  image: 2,
  video: 3
};

class RedditFeed extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      is_loaded: false,
      submissions: [],
      sort: "rating",
      finished_loading: false,
      skip: 0
    };
  }

  async componentDidMount() {
    while (this.state.finished_loading == false && this.state.error == null) {
      try {
        const response = await fetch("/api/reddit-feed/?skip=" + this.state.skip)
        const res = await response.json();
        let current_submissions = this.state.submissions;

        if (res.length == 0)
          this.setState({finished_loading: true})
        else {
          current_submissions.push(...res);
          this.setState({ 
            is_loaded: true,
            submissions: current_submissions,
            skip: this.state.skip + 10
          });
        console.log(current_submissions);
        }
      } catch (error) {
        this.setState({
          error: error
        })
      }
    }
  }

  render_comments(index) {
    console.log(index);
    var submissions = this.state.submissions;
    submissions[index].show_comments = true;
    this.setState({
      submissions: submissions
    });
    console.log(this.state.submissions[index])
  }

  render() {
    const { error, is_loaded, submissions, sort, finished_loading, skip } = this.state;
    if (error) {
      return ({error})
    }
    else if (!is_loaded) {
      return ("Loading...")
    } 
    else {
      for (let i=0; i < submissions.length; i++) {
        let submission = submissions[i];
        if (submission.media_type == SumbissionMediaType.video) {
          submission.media_html = <video controls src={submission.url}></video>;
        } else if (submission.media_type == SumbissionMediaType.image) {
          submission.media_html = <img src={submission.url}/>;
        } else {
          submission.media_html = <a href={submission.url}>Source</a>;
        }
        if (submission.rating >= 1000) {
          submission.rating = Math.floor(submission.rating / 1000) + "k";
        }
        submission.show_comments = false;
      }

      return (
          <div>
            {submissions.map((submission, index) => {
              return (
                <div class="submission" key={index.toString()}>
                  <hr></hr>
                  <h2>{submission.title}</h2>
                  <span> (rating {submission.rating})</span>
                  <p>{submission.text}</p>
                  <div>{submission.media_html}</div>
                  <button onClick={() => this.render_comments(index)}>Comments</button>
                  {submission.show_comments ? <p>show_comments</p> : <p>no comments</p>}
                </div>
              )
            })}
          </div>
        )
    }
  }
}

const domContainer = document.querySelector('#reddit_feed');
const root = ReactDOM.createRoot(domContainer);
root.render(e(RedditFeed));