import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageComponent } from './image.component';
import { ComponentRef, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ImageService } from '../../_services/image.service';
import { ButtonComponent, ButtonType } from '../button/button.component';
import { By } from '@angular/platform-browser';
import { of, throwError } from 'rxjs';

describe('ImageComponent', () => {
  let component: ImageComponent;
  let componentRef: ComponentRef<ImageComponent>;
  let fixture: ComponentFixture<ImageComponent>;

  const imageService = jasmine.createSpyObj('ImageService', [
    'get'
  ]);
  imageService.get.and.returnValue(of("ksfvbdk"))

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImageComponent],
      providers: [
        {
          provide: ImageService,
          useValue: imageService
        },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageComponent);
    component = fixture.componentInstance;
    componentRef = fixture.componentRef;

    const fetchSpy = spyOn(component, 'fetch');

    imageService.get.calls.reset();
    imageService.get.and.returnValue(of('image'));
    fetchSpy.calls.reset();
  });

  it('Should create', () => {
    expect(component).toBeTruthy();
  });

  it('Should make the image get call on fetch with less 80', () => {
    const fixture = TestBed.createComponent(ImageComponent);
    const component = fixture.componentInstance;
    const componentRef = fixture.componentRef;

    componentRef.setInput("id", "id");
    componentRef.setInput("icon", "icon");
    componentRef.setInput("size", "50");
    componentRef.setInput("alt", "alt");

    component.fetch("id", 50);

    expect(imageService.get).toHaveBeenCalledOnceWith("id", "80");
  });

  it('Should make the image get call on fetch with >80 < 160', () => {
    const fixture = TestBed.createComponent(ImageComponent);
    const component = fixture.componentInstance;
    const componentRef = fixture.componentRef;

    componentRef.setInput("id", "id");
    componentRef.setInput("icon", "icon");
    componentRef.setInput("size", "120");
    componentRef.setInput("alt", "alt");

    component.fetch("id", 120);

    expect(imageService.get).toHaveBeenCalledOnceWith("id", "160");
  });


  it('Should make the image get call on fetch with >160 < 320', () => {
    const fixture = TestBed.createComponent(ImageComponent);
    const component = fixture.componentInstance;
    const componentRef = fixture.componentRef;

    componentRef.setInput("id", "id");
    componentRef.setInput("icon", "icon");
    componentRef.setInput("size", "120");
    componentRef.setInput("alt", "alt");

    component.fetch("id", 220);

    expect(imageService.get).toHaveBeenCalledOnceWith("id", "320");
  });

  it('Should make the image get call on fetch with >320', () => {
    const fixture = TestBed.createComponent(ImageComponent);
    const component = fixture.componentInstance;
    const componentRef = fixture.componentRef;

    componentRef.setInput("id", "id");
    componentRef.setInput("icon", "icon");
    componentRef.setInput("size", "120");
    componentRef.setInput("alt", "alt");

    component.fetch("id", 420);

    expect(imageService.get).toHaveBeenCalledOnceWith("id", "");
  });

  it('Should revoke the previous object URL when fetching a new image', () => {
    const imageFixture = TestBed.createComponent(ImageComponent);
    const imageComponent = imageFixture.componentInstance;
    const createObjectUrlSpy = spyOn(URL, 'createObjectURL').and.returnValues('first-url', 'second-url');
    const revokeObjectUrlSpy = spyOn(URL, 'revokeObjectURL');

    imageComponent.fetch('id', 80);
    imageComponent.fetch('id', 80);

    expect(createObjectUrlSpy).toHaveBeenCalledTimes(2);
    expect(revokeObjectUrlSpy).toHaveBeenCalledOnceWith('first-url');
  });

  it('Should clear image data when fetching fails', () => {
    const imageFixture = TestBed.createComponent(ImageComponent);
    const imageComponent = imageFixture.componentInstance;
    imageService.get.and.returnValue(throwError(() => new Error('failed')));
    const errSpy = spyOn(console, 'error');

    imageComponent.fetch('id', 80);

    expect(console.error).toHaveBeenCalledWith(
      'Failed to load image \'id\' at size 80:',
      Error('failed')
    );
    expect(imageComponent.imageData()).toBeNull();

    errSpy.calls.reset();
  });

  it('Should revoke the object URL on destroy', () => {
    const imageFixture = TestBed.createComponent(ImageComponent);
    const imageComponent = imageFixture.componentInstance;
    spyOn(URL, 'createObjectURL').and.returnValue('image-url');
    const revokeObjectUrlSpy = spyOn(URL, 'revokeObjectURL');

    imageComponent.fetch('id', 80);
    imageComponent.ngOnDestroy();

    expect(revokeObjectUrlSpy).toHaveBeenCalledOnceWith('image-url');
  });

  it('View: Should set content on id', () => {
    componentRef.setInput("id", "id");
    componentRef.setInput("icon", "icon");
    componentRef.setInput("size", 50);
    componentRef.setInput("alt", "alt");
    component.imageData.set("data:image/png;base64,abc");

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(root.classes['content']).toBe(true);
    expect(root.children.length).toBe(1);

    const buttonElement = fixture.debugElement.query(By.directive(ButtonComponent));
    const imageElement = fixture.debugElement.query(By.css('img'));

    expect(imageElement.attributes['referrerpolicy']).toBe('no-referrer');
    expect(imageElement.classes['img']).toBe(true);
    expect(imageElement.attributes['src']).toBe('data:image/png;base64,abc');
    expect(imageElement.attributes['width']).toBe('50');
    expect(imageElement.attributes['height']).toBe('50');
    expect(imageElement.attributes['alt']).toBe('alt');

    expect(buttonElement).toBeNull();

    expect(component.fetch).toHaveBeenCalledOnceWith("id", 50);
  });

  it('View: Should set content on no id', () => {
    componentRef.setInput("id", "");
    componentRef.setInput("icon", 'iconname');
    componentRef.setInput("size", "50");
    componentRef.setInput("alt", "alt");

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(root.classes['content']).toBe(true);
    expect(root.children.length).toBe(1);

    const buttonElement = fixture.debugElement.query(By.css('app-button'));
    const imageElement = fixture.debugElement.query(By.css('img'));

    expect(imageElement).toBeNull();

    const button = buttonElement.componentInstance as ButtonComponent;
    expect(button.type()).toBe(ButtonType.SECONDARY_ICON);
    expect(button.icon()).toBe('iconname' as never);
    expect(button.iconSize()).toBe(43.75);

    expect(component.fetch).not.toHaveBeenCalled();
  });

  it('View: Should set loading layout on id and no imageData', () => {
    componentRef.setInput("id", "id");
    componentRef.setInput("icon", 'iconname');
    componentRef.setInput("size", 50);
    componentRef.setInput("alt", "alt");
    component.imageData.set(null);

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(root.classes['content']).toBe(true);
    expect(root.children.length).toBe(1);

    const buttonElement = fixture.debugElement.query(By.css('app-button'));
    const imageElement = fixture.debugElement.query(By.css('img'));

    const loadingElement = root.query(By.css('div'));

    expect(imageElement).toBeNull();
    expect(buttonElement).toBeNull();

    expect(loadingElement.classes["loading-spinner"]).toBe(true);
    expect(loadingElement.styles["width"]).toBe("70px");
    expect(loadingElement.styles["height"]).toBe("70px");

    const spinnerElement = loadingElement.query(By.css('div'));
    expect(spinnerElement.classes["spinner"]).toBe(true);

    expect(component.fetch).toHaveBeenCalledOnceWith("id", 50);
  });
});

