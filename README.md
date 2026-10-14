# ShowcaseCLI
A simple tool developed to help make little screenshots big!

More specifically allowing for small sub-section screenshots of UI panels like this: 

<img width="300" alt="suspension-gizmos" src="https://github.com/user-attachments/assets/bbbe8283-9b42-42ca-a081-179c87041f05" />

A standardized size with a few controllable options, in bulk: 

<img width="1920" height="1080" alt="suspension-gizmos_showcase" src="https://github.com/user-attachments/assets/a515f005-187e-41c6-981e-471dfa114688" />


## How to use
Clone the repo down and if you're on Windows just run the batch file:

<img width="750" height="369" alt="image" src="https://github.com/user-attachments/assets/6e910fe7-a1ed-4049-9b41-fdebbb8b3b5b" />

Point the source directory to a folder with all of your base screenshots: 

<img width="472" height="97" alt="image" src="https://github.com/user-attachments/assets/b6bb7c37-2623-460f-a66d-4ff28acaa982" />

You will see an output of all images in the folder, and must confirm [Y] before proceeding! The next step is deciding if you want the background to be a color [0] or an image [1].

For this example, I'll pick a color, but with the image option you can point it to a specific image to use, which can be blurred and faded out for good measure!

Here's an example showcasing selecting a background color:

<img width="476" height="125" alt="image" src="https://github.com/user-attachments/assets/579a73b6-2f36-45d6-8912-9db0951c8b4e" />

Go ahead and confirm your options and add a rounded edge if you'd like, this will add rounding to the internal screenshot: 

<img width="475" height="152" alt="image" src="https://github.com/user-attachments/assets/4032d1b8-255f-4ef3-b2b9-f5d4c5514cae" />

Finally, confirm you are ready to bulk process the entire folder: 

<img width="466" height="123" alt="image" src="https://github.com/user-attachments/assets/5810d017-88b7-4f32-9891-ecc51864f1aa" />

Once complete, you will end up with a `/showcase` directory with all of the converted images:

<img width="727" height="134" alt="image" src="https://github.com/user-attachments/assets/bb298b93-381a-4457-b0b3-4228fb504fb8" />


## Why did I need this
Unity assets require screenshots when listed on the Unity asset store, and I often want to showcase small gizmos, or the inspector panels, which when snipped are quite small. 

Not long ago, an enforcement change was made where all screenshots must be 1920x1080 and as a result these small snips wouldn't be allowed. 

This is one of the main reasons I decided a tool like this would be handy, meeting the requirement, but still leaving focus where it belongs! 

## Future
Although I don't see too much active work left here, if I was to add anything I would add the ability to caption images, however, I'm unsure how to implement this into automated batches, perhaps filenames processed into human readible outputs or something like that. 

