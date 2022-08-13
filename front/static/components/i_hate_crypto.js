'use strict';

const e = React.createElement;

var price_formatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD'
});

var percent_formatter = new Intl.NumberFormat('default', {
  style: 'percent',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

class CryptoListing extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      is_loaded: false,
      data: null
    };
  }

  async componentDidMount() {
    try {
      const response = await fetch("/api/i-hate-crypto/");
      const res = await response.json();
      this.setState({
        is_loaded: true,
        data: res
      });
    } catch (error) {
        this.setState({
          is_loaded: true,
          error: error
        })
      }
  }


  render() {
    const { error, is_loaded, data } = this.state;
    
    if (error) {
      console.log(error);
      return ({error})
    }
    else if (!is_loaded) {
      return ("Loading...")
    } 
    else {
      var last_time_fetched = new Date(data["status"]["timestamp"]).toDateString();
      var coins = Array.from(data["data"]).filter(coin => !coin.tags.includes("stablecoin"));

      return (
          <div>
            <p>Last time fetched: {last_time_fetched}</p>
            <table className="listing">
              <thead>
                <tr>
                  <th scope="col">Coin</th>
                  <th scope="col">Price</th>
                  <th scope="col">Change</th>
                </tr>
              </thead>
              <tbody>
                {coins.map((coin) => {
                  return (
                    <tr>
                      <td>{coin.name}</td>
                      <td>{price_formatter.format(coin.quote.USD.price)}</td>
                      <td className={coin.quote.USD.percent_change_24h < 0 ? "win" : "lose"}>{percent_formatter.format(coin.quote.USD.percent_change_24h/10)}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )
    }
  }
}

const domContainer = document.querySelector('#i_hate_crypto');
const root = ReactDOM.createRoot(domContainer);
root.render(e(CryptoListing));