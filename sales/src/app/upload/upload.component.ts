// import { Component } from '@angular/core';
// import { HttpClient } from '@angular/common/http';

// @Component({
//   selector: 'app-upload',
//   templateUrl: './upload.component.html',
//   styleUrls: ['./upload.component.css']
// })
// export class UploadComponent {
//   selectedFile: File | null = null;

//   constructor(private http: HttpClient) { }

//   onFileSelected(event: any) {
//     this.selectedFile = event.target.files[0];
//   }

//   uploadFile() {
//     if (this.selectedFile) {
//       const formData = new FormData();
//       formData.append('file', this.selectedFile);

//       this.http.post('http://127.0.0.1:5000/upload', formData)
//         .subscribe(
//           response => {
//             console.log('File uploaded successfully');
//           },
//           error => {
//             console.log('Error uploading file:', error);
//           }
//         );
//     }
//   }
// }



import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {
  selectedFile !: File;
  selectcheck !: string;
  yearFrom !: number;
  yearTo !: number;
  yearForMonthly !: number;
  yearForDaily !: number;
  monthForDaily !: number;
  dayForDaily !:number;
  numForMonthly!:number;
  yearForweekly !:number;
  numForweekly !:number;
  em !: string;


  constructor(private http: HttpClient, private router :Router) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  upFile() {
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('selectcheck', this.selectcheck);
      // formData.append('yearFrom', this.yearFrom.toString());
      // formData.append("yearTo", this.yearTo.toString()) 
      if (this.selectcheck === 'yearly') {
        formData.append('yearFrom', this.yearFrom.toString());
        formData.append('yearTo', this.yearTo.toString());
      }

      if (this.selectcheck === 'monthly') {
        formData.append('yearForMonthly', this.yearForMonthly.toString());
        formData.append('numForMonthly', this.numForMonthly.toString());

      }
      if (this.selectcheck === 'weekly'){
        formData.append('yearForweekly', this.yearForweekly.toString());
        formData.append('numForweekly', this.numForweekly.toString());     
      }
      if (this.selectcheck === 'daily') {
        formData.append('yearForDaily', this.yearForDaily.toString());
        formData.append('monthForDaily', this.monthForDaily.toString());
        formData.append('dayForDaily', this.dayForDaily.toString());
      }

      this.http.post<any>('http://127.0.0.1:5000/upload', formData).subscribe(
        (response: any) => {
          if (response.error) {
            console.log(response.error);
          } else {
            this.em = response.success;
            if (this.em === 'successful') {
              this.router.navigate(['/powerbi']);
            }
          }
        },
        (error) => {
          console.log(error);
        }
      );
    }
  }
}