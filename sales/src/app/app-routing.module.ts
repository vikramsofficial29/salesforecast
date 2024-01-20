import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { UploadComponent } from './upload/upload.component';
import { PowerbiComponent } from './powerbi/powerbi.component';
import { DashComponent } from './dash/dash.component';

const routes: Routes = [
  {path:'home', component:HomeComponent},
  { path : '', redirectTo : 'home', pathMatch:'full'},
  { path : 'signup',component:SignupComponent},
  { path : 'login',component:LoginComponent},
  { path : 'upload',component:UploadComponent},
  { path : 'powerbi',component:PowerbiComponent},
  { path : 'dash',component:DashComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
