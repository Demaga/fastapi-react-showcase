'use strict';

const e = React.createElement;

class WhoSaidThatPoll extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: []
    };
  }

  componentDidMount() {
    fetch("/api/who-said-that/")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  render() {
    const { error, isLoaded, items } = this.state;
    if (error) {
      return ({error})
    }
    else if (!isLoaded) {
      return ("Loading...")
    } 
    else {
      return (
          <div>
            <p>{JSON.stringify(items)}</p>
          </div>
        )
    }
  }
}

const domContainer = document.querySelector('#who_said_that');
const root = ReactDOM.createRoot(domContainer);
root.render(e(WhoSaidThatPoll));