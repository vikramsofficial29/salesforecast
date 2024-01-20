import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-powerbi',
  templateUrl: './powerbi.component.html',
  styleUrls: ['./powerbi.component.css']
})
export class PowerbiComponent {
  emessage !: string;
  chartLabels: string[] = [];
  chartValues: number[] = [];
  a: string = '10';

  constructor(private http: HttpClient) {} 
  ngOnInit():void {
    console.log('submitted');
    console.log(this.a);

    this.http.post<any>('http://127.0.0.1:5000/powerbi', { a: this.a }).subscribe(
      (response: any) => {
        if (response.error) {
          this.emessage = response.error;
          console.log(response.error);

        } else {
          console.log(response.message);
          this.chartLabels = response.chartlabels;
          this.chartValues = response.chartvalues;
        }
      },
      (error) => {
        console.log('Error:', error);
      }
    );
  }
}