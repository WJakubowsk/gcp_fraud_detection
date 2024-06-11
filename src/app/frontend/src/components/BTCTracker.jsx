import React, { useState, useEffect } from 'react';
import Chart from 'react-apexcharts';
import axios from 'axios';


const BinanceCoinTracker = ({plot, selectedPeriod}) => {
  const [historicalData, setHistoricalData] = useState([]);
  const [currentPrice, setCurrentPrice] = useState(null);
  const [priceChange, setPriceChange] = useState(null);

  useEffect(() => {
    fetchCurrentPrice();
    const endDate = new Date().getTime();
    let startDate;
    let interval;
    switch (selectedPeriod) {
      case '12h':
        startDate = endDate - 12 * 60 * 60 * 1000;
        interval = '1m';
        break;
      case '1w':
        startDate = endDate - 7 * 24 * 60 * 60 * 1000;
        interval = '1h';
        break;
      case '3M':
        startDate = new Date(endDate);
        startDate.setMonth(startDate.getMonth() - 3);
        startDate = startDate.getTime();
        interval = '1d';
        break;
      default:
        startDate = endDate - 24 * 60 * 60 * 1000;
    }
    fetchData(interval, startDate, endDate);
  }, [selectedPeriod]);

  useEffect(() => {
    fetchCurrectPercentage();
  }, [historicalData, currentPrice]);

  const fetchData = async (period, startDate, endDate) => {
    try {
      const response = await axios.get(`https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=${period}&startTime=${startDate}&endTime=${endDate}&limit=1000`);
      const data = response.data.map(item => ({
        x: new Date(item[0]),
        y: [parseFloat(item[1]), parseFloat(item[2]), parseFloat(item[3]), parseFloat(item[4])]
      }));
      setHistoricalData(data);
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  };

  const fetchCurrectPercentage = async () => {
    try {
      const startPrice = historicalData.length > 0 ? historicalData[0].y[3] : null;
      const current = currentPrice;
      if (startPrice && current) {
        const change = ((current - startPrice) / startPrice) * 100;
        setPriceChange(change.toFixed(3));
      }
    } catch (error) {
      console.error('Error fetching current price: ', error);
    }
  };

  const fetchCurrentPrice = async () => {
    try {
      const response = await axios.get(`https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT`);
      setCurrentPrice(parseFloat(response.data.price));
      fetchCurrectPercentage();
    } catch (error) {
      console.error('Error fetching current price: ', error);
    }
  };

  return (
    <div>
      {plot ? (
        <div>
          <div style={{ width: '100%', height: '40vh' }}>
            <Chart
              options={{
                chart: {
                  type: 'candlestick',
                  toolbar: {
                    show: false
                  },
                  colors: ['#77B6EA', '#545454', '#FEB019', '#FF4560'],
                },
                xaxis: {
                  type: 'datetime',
                  labels: {
                    style: {
                      colors: '#ffffff',
                      fontSize: '15px',
                    },
                  },
                },
                yaxis: {
                  tooltip: {
                    enabled: true,
                    intersect: true,
                  },
                  labels: {
                    style: {
                      colors: '#ffffff',
                      fontSize: '100%',
                    },
                  },
                },
                tooltip: {
                  theme: 'dark',
                  x: {
                    format: 'dd MMM yyyy HH:mm:ss'
                  }
                }
              }}
              series={[{ data: historicalData }]}
              type="candlestick"
              height="100%"
            />
          </div>
        </div>
      ) : (
        <div style={{fontSize: '130%'}}>
          <p>Current BTC Price: ${currentPrice}</p>
          <p>Last {selectedPeriod} Change: {priceChange !== null ? (priceChange > 0 ? `+${priceChange}%` : `${priceChange}%`) : 'Loading...'}</p>
        </div>
      )}
    </div>
  );

};

export default BinanceCoinTracker;
