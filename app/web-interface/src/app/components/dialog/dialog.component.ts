import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, ElementRef, Input, output, TemplateRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-dialog',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: 'dialog.component.html',
  styleUrls: ['dialog.component.css'],
})
export class DialogComponent implements AfterViewInit {
  @Input()
  content!: TemplateRef<any>;

  @ViewChild('dialogFrame')
  dialogFrame!: ElementRef<HTMLDivElement>;

  closeEmitter = output<boolean>();

  ngAfterViewInit(): void {
    this.dialogFrame.nativeElement.focus();
  }

  onBackgroundClick(event: Event): void {
    if (event instanceof MouseEvent) {
      if (event.target === event.currentTarget) {
        this.closeEmitter.emit(true);
      }
    } else if (event instanceof KeyboardEvent) {
      if (event.key === 'Escape') {
        this.closeEmitter.emit(true);
      }
    }
  }
}
