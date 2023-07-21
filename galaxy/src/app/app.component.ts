import { Component } from '@angular/core';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000'
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'galaxy';
}
