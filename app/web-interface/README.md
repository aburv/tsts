![Generic badge](https://img.shields.io/badge/Build-PASSED-green.svg)  ![Generic badge](https://img.shields.io/badge/Coverage-100%25-green.svg) ![Generic badge](https://img.shields.io/badge/Angular-Typescript-green.svg)

# Browser Interface
   An Angular application -V20.3.2

   Typescript -V5.9.2

## Development server

### Prerequisites:

* Env configs
setup the values at `/src/environments/environment.ts`

* Install Dependencies

```commandline
npm install
```

* Run locally.

```commandline
npm run start
```

Check ` http://localhost:4200/ ` in any browser

## Code Quality

### Lint

```commandline
npm run lint
```

Maintain 0 errors and minimize the warnings as much as possible

## Testing

### Unit Testing

Unit tests are present in same folder next to actual file. 
Component and functional level testing.

Install chrome.exe to run the test 

```commandline
npm run test
```

set ` --watch=true ` to test script in package.json

View Code Coverage in html format

`/coverage/web-interface/index.html`

## UI Component Usage 

* ### Button

```TS
type: ButtonType
title: string
icon: Icon
onClick(event: MouseEvent){}
```

```HTML
<app-button 
   [type]="type" 
   [text]="title" 
   [icon]="icon" 
   (click)="onClick($event)"
></app-button>
```

* ### Chipset

```TS
options: Array<{id: string, text:string}>
selected: Array<string>
onClick(selectedId: string){}
```
```HTML
<app-chip-set 
   [selected]="selected" 
   [options]="options" 
   (childEmitter)="onClick($event)"
></app-chip-set>
```

* ### Dialog

```TS
isDialogOn: boolean
```
```HTML
<ng-template #dialogContent>
   <div style="position: relative">
      <!--Content -->
   </div>
</ng-template>

@if (isDialogOn) {
<app-dialog 
   [content]="dialogContent" 
   (closeEmitter)="isDialogOn=!$event"
></app-dialog>
}
```

* ### Icon

```TS
iconName: Icon
size: number
```
```HTML
<app-icon
   [name]="iconName"
   [size]="size"
></app-icon>
```

Image
```TS
imageId: string
icon: Icon
size: number
```
```HTML
<app-image 
   [size]="size" 
   [id]="imageId" 
   [icon]="icon" 
   [alt]="altText">
</app-image>
```
* ### Input Date

```TS
title: string
value: DateTime
min: DateTime
max: DateTime
```
```HTML
<app-input-date 
   [title]="title" 
   [value]="value" 
   [min]="min" 
   [max]="max"
></app-input-date>
```

* ### Input Text
```TS
type: InputSize
title: string
placeholder: string
value: string
validator: Validator
onClick(text: string){}
```

```HTML
<app-input 
   [placeholder]="placeholder" 
   [title]="title" 
   [value]="value" 
   [type]="type" 
   [validator]="validator" 
   (childEmitter)="onClick($event)"
></app-input>
```

* ### Toggler

```TS
options: Array<string>
selected: string
onClick(selectedText: string){}
```
```HTML
<app-toggler 
   [selected]="selected" 
   [options]="options" 
   (childEmitter)="onClick($event)"
></app-toggler>
```

## Happy UI coding