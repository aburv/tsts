import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { ButtonComponent } from './components/button/button.component';
import { ChipSetComponent } from './components/chip-set/chip-set.component';
import { DialogComponent } from './components/dialog/dialog.component';
import { IconComponent } from './components/icon/icon.component';
import { ImageComponent } from './components/image/image.component';
import { InputDateComponent } from './components/input-date/input-date.component';
import { InputComponent } from './components/input-text/input.component';
import { TogglerComponent } from './components/toggler/toggler.component';

import { UserButtonComponent } from './components/user-button/user-button.component';

import { DashboardComponent } from './pages/dashboard/dashboard.component';

@NgModule({
  declarations: [
    AppComponent,
    ButtonComponent,
    ChipSetComponent,
    DialogComponent,
    IconComponent,
    ImageComponent,
    InputDateComponent,
    InputComponent,
    TogglerComponent,
    UserButtonComponent,
    DashboardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
