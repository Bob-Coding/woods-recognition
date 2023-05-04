import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.apiUrl,
});

export default ({ app }, inject) => {
  inject('axios', instance);
};
