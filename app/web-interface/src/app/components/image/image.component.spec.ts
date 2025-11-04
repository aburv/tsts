import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageComponent } from './image.component';
import { ComponentRef, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ImageService } from 'src/app/_services/image.service';
import { By } from '@angular/platform-browser';
import { of } from 'rxjs';

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
      schemas:[CUSTOM_ELEMENTS_SCHEMA]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageComponent);
    component = fixture.componentInstance;
    componentRef = fixture.componentRef;

    const fetchSpy = spyOn(component, 'fetch');

    fetchSpy.calls.reset();
  });

  it('Should create', () => {
    expect(component).toBeTruthy();
  });

  it('Should make the image get call on fetch', () => {
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

  it('View: Should set content on id', () => {
    componentRef.setInput("id", "id");
    componentRef.setInput("icon", "icon");
    componentRef.setInput("size", 50);
    componentRef.setInput("alt", "alt");

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));
   
    expect(root.classes['user']).toBe(true);
    expect(root.children.length).toBe(1);

    const buttonElement = fixture.debugElement.query(By.css('app-button'));
    const imageElement = fixture.debugElement.query(By.css('img'));

    expect(imageElement.attributes['referrerpolicy']).toBe('no-referrer');
    expect(imageElement.classes['user-img']).toBe(true);
    expect(imageElement.attributes['src']).toBe('');
    expect(imageElement.attributes['width']).toBe('50');
    expect(imageElement.attributes['height']).toBe('50');
    expect(imageElement.attributes['alt']).toBe('alt');

    expect(buttonElement).toBeNull();

    expect(component.fetch).toHaveBeenCalledOnceWith("id", 50);
  });

  it('View: Should set content on no id', () => {
    componentRef.setInput("id", "");
    componentRef.setInput("icon", { name: 'iconname' });
    componentRef.setInput("size", "50");
    componentRef.setInput("alt", "alt");

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));
   
    expect(root.classes['user']).toBe(true);
    expect(root.children.length).toBe(1);

    const buttonElement = fixture.debugElement.query(By.css('app-button'));
    const imageElement = fixture.debugElement.query(By.css('img'));

    expect(imageElement).toBeNull();

    expect(buttonElement.componentInstance.type()).toBe('secondary icon');
    expect(buttonElement.componentInstance.icon()).toEqual({ name: 'iconname' });
    expect(buttonElement.componentInstance.iconSize()).toBe(43.75);

    expect(component.fetch).not.toHaveBeenCalled();
  });
});

