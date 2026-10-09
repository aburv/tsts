import { Component, effect, input, inject, OnDestroy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ImageService } from '../../_services/image.service';
import { ButtonComponent, ButtonType } from '../button/button.component';
import { Icon } from '../icon/icon.component';

@Component({
  selector: 'app-image',
  standalone: true,
  imports: [
    CommonModule,
    ButtonComponent,
  ],
  templateUrl: './image.component.html',
  styleUrl: './image.component.css'
})
export class ImageComponent implements OnDestroy {
  private image = inject(ImageService);

  readonly ButtonType = ButtonType

  id = input.required<string>();
  icon = input.required<Icon>();
  size = input.required<number>();
  alt = input.required<string>();

  imageData= signal<string | null>(null);
  private objectUrl: string | null = null;

  constructor() {
    effect(() => {
      const id = this.id();
      const size = this.size();

      if (id && id !== "") {
        this.fetch(id, size);
      }
    })
  }

  fetch(id: string, size: number): void {
    let imgRes = size.toString();
    if (size <= 80) {
      imgRes = "80"
    }
    else if (size <= 160) {
      imgRes = "160"
    }
    else if (size <= 320) {
      imgRes = "320"
    }
    else {
      imgRes = ""
    }
    this.image.get(id, imgRes).subscribe({
      next: (data: any) => {
        const blob = new Blob([data]);

        if (this.objectUrl !== null) {
          URL.revokeObjectURL(this.objectUrl);
        }
        this.objectUrl = URL.createObjectURL(blob);
        this.imageData.set(this.objectUrl);
      },
      error: (error) => {
        console.error(`Failed to load image '${id}' at size ${imgRes}:`, error);
        this.imageData.set(null);
      }
    });
  }

  ngOnDestroy(): void {
    if (this.objectUrl !== null) {
      URL.revokeObjectURL(this.objectUrl);
    }
  }
}
