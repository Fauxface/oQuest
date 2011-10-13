import os
import sys
import math
import random
#import traceback
import string
import json
import pygame
from pygame.locals import *


class Game:
    """ Class handling the game startup, loop, and object management
    """
    def __init__(self):
        print('Init')
        
        self.screenWidth = 800
        self.screenHeight = 600
        self.windowTitle = 'OwlQuest: Sugoi Monogatari'
        
        pygame.init()
        self.setVariables()
        self.loadAttributes() # Loads objects' attributes data
        self.window = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption(self.windowTitle)
        self.screen = pygame.display.get_surface()  
        self.clock = pygame.time.Clock()
        self.exit = False
    
    def setVariables(self):
        """ Player input move rates
        """
        # TODO: Move into Actor to be loaded with the player
        self.xMoveRate = 0.001
        self.yMoveRate = 0.001
        self.zMoveRate = 0.001
        self.rRate = 0.5
        self.actorNum = 0 # Unique ID for actors
    
    def main(self):
        print('Main')
        self.setupStage()
        
        while self.exit == False:
            self.handleInput(pygame.event.get(), pygame.key.get_pressed())
            self.updateActors()
            self.drawOutput()
            self.clock.tick(60) # FPS
        
        print('Exiting')
        
    def loadAttributes(self):
        try:
            f = open('data/objects.json', 'r')
            self.attributesList = json.loads(f.read())
            f.close()
        except IOError as e:
            print('loadAttributes: Error loading object attributes file: {}'.format(e))
            filePath = self.dataPath + self.objectsFile
            self.attributesList = {}
            
            if os.path.exists(self.dataPath) == False:
                print('loadAttributes: Creating object attributes file path:{}'.format(self.dataPath))
                os.mkdirs(self.dataPath)
            elif os.path.isfile(filePath) == False:
                print('loadAttributes: Touching object attributes file:{}'.format(self.objectsFile))
                f = open(self.objectsFile, 'w')
                f.close()
        except BaseException as e:
            print('loadAttributes: Error loading object attributes file: {}'.format(e))
        
    def getAttributes(self, id):
        """
        For Actors to get a set of object attributes from an already loaded attributes list
        We only have to load the list once this way
        """
        return self.attributesList["objects"][str(id)]
        
    def setupStage(self):
        self.createBackground()
        self.spritesInitDetails = list()
        self.spritesInitDetails.append(('player', 0, [0, 0, 0, 0]))
        self.spritesInitDetails.append(('enemy', 3, [50, 50, 0, 0])) # Debug enemy
        self.allSprites = []
        self.allSpritesGroup = pygame.sprite.RenderUpdates()
        
        for sprite in self.spritesInitDetails:
            # Create sprite objects: name, id(type), starting coordinates
            print(sprite)
            self.createActor(sprite[0], sprite[1], sprite[2])
        
        pygame.display.flip()
    
    def createBackground(self):
        self.background = pygame.Surface((self.screenWidth, self.screenHeight))
        self.background.fill((128, 128, 128))
        self.screen.blit(self.background, (0,0))
        
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("OwlQuest: Sugoi Monogatari", 1, (10, 10, 10))
            textPos = text.get_rect(centerx=self.screen.get_width()/2)
            self.screen.blit(text, textPos)
    
    def createActor(self, name, id, coord, momentum=[0,0,0,0]):
        print('Creating actor')
        actorIndex = len(self.allSprites)
        newActor = Actor(self.actorNum, actorIndex, name, id, coord, momentum)
        #self.allSprites[self.actorNum] = newActor
        self.allSprites.append(newActor)
        self.allSpritesGroup.add(newActor)
        
        if name == 'player':
            self.playerSprite = self.allSprites[-1]
            #self.playerSprite = self.allSprites[self.actorNum]
        
        self.actorNum += 1
    
    def deleteActor(self, actorObject):
        #del self.allSprites[actorNum]
        #x = len(self.allSprites)
        try:
            print('Destroying {}'.format(actorObject))
            actorObject.remove(self.allSpritesGroup)
            self.allSprites.remove(actorObject)
        except BaseException as e:
            print('Game: deleteActor: Error deleting Actor {}: {}'.format(actorObject, e))
        #print('{} {}'.format(x, len(self.allSprites))
    
    def handleInput(self, events, key):
        # Pump syncs pygame's event handler with states of input devices
        pygame.event.pump()
        
        kAddEngine = pygame.K_w
        kMinEngine = pygame.K_s
        kAddThrust = K_LSHIFT
        kMinThrust = K_LCTRL
        kAddR = pygame.K_d
        kMinR = pygame.K_a
        kAddY = pygame.K_r
        kMinY = pygame.K_f
        kAddX = pygame.K_e
        kMinX = pygame.K_q
        kAddZ = pygame.K_SPACE
        kMinZ = pygame.K_c
        kFire = pygame.MOUSEBUTTONDOWN
        kReset = pygame.K_RETURN
        kQuit = pygame.K_ESCAPE
        
        # self.playerSprite is the player object, move(x, y, z, rotation)
        # Y-Axis
        if key[kAddY] and key[kMinY]:
            pass
        elif key[kAddY]:
            self.playerSprite.move((0, self.yMoveRate * -1, 0, 0))
        elif key[kMinY]:
            self.playerSprite.move((0, self.yMoveRate, 0, 0))
        
        # X-Axis
        if key[kAddX] and key[kMinX]:
            pass
        elif key[kMinX]:
            self.playerSprite.move((self.xMoveRate * -1, 0, 0, 0))
        elif key[kAddX]:
            self.playerSprite.move((self.xMoveRate, 0, 0, 0))
        
        # Z-Axis
        if key[kMinZ] and key[kAddZ]:
            pass
        elif key[kMinZ]:
            self.playerSprite.move((0, 0, self.zMoveRate * -1, 0))
        elif key[kAddZ]:
            self.playerSprite.move((0, 0, self.zMoveRate, 0))
        
        # Rotation
        if key[kMinR] and key[kAddR]:
            pass
        elif key[kAddR]:
            self.playerSprite.move((0, 0, 0, self.rRate * -1))
        elif key[kMinR]:
            self.playerSprite.move((0, 0, 0, self.rRate))
        
        # Thrust
        if key[kAddThrust] and key[kMinThrust]:
            pass
        elif key[kAddThrust]:
            self.playerSprite.thrust(1)
        elif key[kMinThrust]:
            self.playerSprite.thrust(-1)
        
        # Engine
        if key[kAddEngine] and key[kMinEngine]:
            pass
        elif key[kAddEngine]:
            self.playerSprite.modifyEngineSpeed(1)
        elif key[kMinEngine]:
            self.playerSprite.modifyEngineSpeed(-1)
        
        # Special Keys
        for event in events:
            if event.type == QUIT:
                # When the 'X' button of the window is clicked
                self.exit = True
            elif event.type == KEYDOWN:
                if event.key == kReset:
                    self.allSprites[0].reset()
                elif event.key == kQuit:
                    self.exit = True
            elif event.type == kFire: #pygame.MOUSEBUTTONDOWN:# and event.button == LEFT:
                self.playerSprite.fire()
            else:
                #print(event)
                pass
    
    def updateActors(self):
        for actor in self.allSprites:
            actor.update()
            #self.screen.blit(pygame.transform.rotozoom(actor.image(), actor.pos()['r'], actor.pos()['s']), actor.rectangle())
    
    def drawOutput(self):
        self.allSpritesGroup.clear(self.screen, self.background)
        
        # Only update changed areas for speed
        dirty = self.allSpritesGroup.draw(self.screen)
        pygame.display.update(dirty)
    
        # flip has something to do with HW acceleration
        #pygame.display.flip()
        #pygame.display.update()



class Actor(pygame.sprite.Sprite):
    """ Class for objects in the game: player, enemies, bullets
    """
    def __init__(self, actorNum, actorIndex, name, id, coord=[0,0,0,0], momentum=[0,0,0,0]):
        """
        actorNum: Unique ID for created Actors
        actorIndex: Position of Actor in game's allSprites list
        name: Debug use
        id: Actor attributes to load
        coord: Initialisation coordinates
        momentum: Initialisation momentum
        """
        # Do I want to keep all the attributes here, or move them into ActorAttachments?
        #try:
        self.actorNum = actorNum
        self.actorIndex = actorIndex
        pygame.sprite.Sprite.__init__(self) # Call sprite initialiser
        self.loadAttributes(id) # Load object attributes from JSON file
        self.setImage()
        self.setRect()
        self.setVariables(coord, momentum)
        self.setDefaultAttachments()
        self.attribute['loaded'] == True
        #except BaseException as e:
            #print('Actor.__init__: Error creating object: {}'.format(e))
    
    def loadAttributes(self, id):
        self.attribute = self.getAttributes(id)
    
    def getAttributes(self, id):
        # Ideally we don't use game but some form of super() to access getAttributes
        return game.getAttributes(id).copy() # Dicts are passed by reference
    
    def createAttachment(self, id, name, coord):
        newAttachment = ActorAttachment(id, name, coord)
        self.attachmentList.append(newAttachment)
        self.attachmentGroup.add(newAttachment)
    
    def setVariables(self, coord, momentum):
        self.attribute['x'] = coord[0]
        self.attribute['y'] = coord[1]
        self.attribute['z'] = coord[2]
        self.attribute['r'] = coord[3]
        self.attribute['xs'] = momentum[0]
        self.attribute['ys'] = momentum[1]
        self.attribute['zs'] = momentum[2]
        self.attribute['rs'] = momentum[3]
        self.attachmentList = []
        self.attachmentGroup = pygame.sprite.RenderUpdates()
    
    def setDefaultAttachments(self):
        # Move to external data file
        if self.attribute['id'] == 0:
            self.createAttachment(2, 'gun', (0,0,0))
            self.createAttachment(2, 'gun', (50,50,0))
    
    def setImage(self):
        self.actorsImagePath = 'i/Actors'
        imageId = self.attribute['imageId']
        self.attribute['image'] = '{}/{}.png'.format(self.actorsImagePath, imageId)
        self.image = pygame.image.load(self.attribute['image']).convert_alpha()
        self.baseImage = self.image
        self.surface = self.image
    
    def setRect(self):
        self.rect = self.surface.get_rect()
        self.rect.x = self.attribute['x']
        self.rect.y = self.attribute['y']
    
    def image(self):
        # See if I can delete these methods
        return self.surface
    
    def attributes(self):
        return self.attribute
    
    def rectangle(self):
        return self.rect
    
    def reset(self):
        print('Reset')
        self.attribute['x'] = 0
        self.attribute['y'] = 0
        self.attribute['z'] = 0
        self.attribute['engineSpeed'] = 0
    
    def fire(self):
        momentum = [self.attribute['xs'], self.attribute['ys'], self.attribute['zs'], 0] # xs, ys, zs, rs
        coord = [self.attribute['x'], self.attribute['y'], self.attribute['z'], self.attribute['r']]
        
        for attachment in self.attachmentList:
            if attachment.getAttachmentAttribute()['name'] == 'gun':
                attachment.fire(coord, momentum)
    
    def thrust(self, dir, coef=None):
        # dir: 1 - forwards, -1 - backwards
        if coef == None:
            coef = self.attribute['thrustSpeed']
            
        radR = math.radians(self.attribute['r'])
        
        # * -1 because (0, 0) is top-left and we have to flip the coordinates
        x = coef * dir * math.sin(radR) * -1
        y = coef * dir * math.cos(radR) * -1
        
        self.attribute['xs'] += x
        self.attribute['ys'] += y
    
    def runEngine(self):
        # Adds thrust on update()
        self.thrust(1, self.attribute['engineSpeed'])
        
    def modifyEngineSpeed(self, dir, accelChange=None):
        if dir == 1:
            accelChange = self.attribute['engineAccel']
        elif dir == -1:
            accelChange = self.attribute['engineDeaccel']
    
        if self.attribute['engineSpeed'] + accelChange > self.attribute['engineMaxAccel']:
            self.attribute['engineSpeed'] = self.attribute['engineMaxAccel']
        elif self.attribute['engineSpeed'] + accelChange < self.attribute['engineMinAccel']:
            self.attribute['engineSpeed'] = self.attribute['engineMinAccel']
        else:
            self.attribute['engineSpeed'] += accelChange
    
    def move(self, coord):
        # Modify Speed & Acceleration
        if coord[0] > 0 and self.attribute['xs'] <= self.attribute['xsMax']:
            self.attribute['xs'] = self.attribute['xs'] + self.attribute['xa']
        elif  coord[0] < 0 and self.attribute['xs'] >= self.attribute['xsMin']:
            self.attribute['xs'] -= self.attribute['xa']
        
        if coord[1] > 0 and self.attribute['ys'] <= self.attribute['ysMax']:
            self.attribute['ys'] += self.attribute['ya']
        elif coord[1] < 0 and self.attribute['ys'] >= self.attribute['ysMin']:
            self.attribute['ys'] -= self.attribute['ya']
        
        if coord[2] > 0 and self.attribute['zs'] <= self.attribute['zsMax']:
            self.attribute['zs'] += self.attribute['za']
        elif coord[2] < 0 and self.attribute['zs'] >= self.attribute['zsMin']:
            self.attribute['zs'] -= self.attribute['za']
        
        if coord[3] > 0 and self.attribute['rs'] <= self.attribute['rsMax']:
            self.attribute['rs'] += self.attribute['ra']
        elif coord[3] < 0 and self.attribute['rs'] >= self.attribute['rsMin']:
            self.attribute['rs'] -= self.attribute['ra']
    
    def updateX(self, xCoord):    
        # Speed
        if self.attribute['xs'] > self.attribute['xsMax']:
            self.attribute['xs'] = self.attribute['xsMax']
        elif self.attribute['xs'] < self.attribute['xsMin']:
            self.attribute['xs'] = self.attribute['xsMin']
        
        newx = self.attribute['x'] + xCoord + self.attribute['xs']
        
        # Boundary, x relative to screen edge
        if newx > self.attribute['xMax'] + game.screenWidth:
            #newx = self.attribute['xMax'] # Uncomment to make it wrap
            newx = self.attribute['xMax'] + game.screenWidth
        elif newx < self.attribute['xMin']:
            newx = self.attribute['xMin']
        
        self.attribute['x'] = newx
    
    def updateY(self, yCoord):
        # Speed
        if self.attribute['ys'] > self.attribute['ysMax']:
            self.attribute['ys'] = self.attribute['ysMax']
        elif self.attribute['ys'] < self.attribute['ysMin']:
            self.attribute['ys'] = self.attribute['ysMin']
        
        newy = self.attribute['y'] + yCoord + self.attribute['ys']
        
        # Boundary, y relative to screen edge
        if newy > self.attribute['yMax'] + game.screenHeight:
            #newy = self.attribute['yMax'] # Uncomment to wrap
            newy = self.attribute['yMax'] + game.screenHeight
        elif newy < self.attribute['yMin']:
            newy = self.attribute['yMin']
        
        self.attribute['y'] = newy
    
    def updateScale(self):
        # Scaling
        if self.attribute['s'] <= self.attribute['sMax'] and self.attribute['s'] >= self.attribute['sMin']:
            newScale = self.attribute['s'] + self.attribute['zs'] / 100 # To make it into a decimal representation of scaling
            
            if newScale > self.attribute['sMax']:
                newScale = self.attribute['sMax']
            elif newScale < self.attribute['sMin']:
                newScale = self.attribute['sMin']
            
            self.attribute['s'] = newScale
        # TODO: Add speed changes for scaling, or change camera height to simulate parallax scrolling
    
    def updateRotation(self, rot):
        # Rotation
        if self.attribute['r'] <= self.attribute['rMax'] and self.attribute['r'] >= self.attribute['rMin']:
            if self.attribute['rs'] > self.attribute['rsMax']:
                self.attribute['rs'] = self.attribute['rsMax']
            elif self.attribute['rs'] < self.attribute['rsMin']:
                self.attribute['rs'] = self.attribute['rsMin']
            
            newRot = self.attribute['r'] + rot + self.attribute['rs']
            
            if newRot > self.attribute['rMax']:
                newRot = self.attribute['rMax']
            elif newRot < self.attribute['rMin']:
                newRot = self.attribute['rMin']
            
            # For unlimited rotation
            if newRot == self.attribute['rMax'] or newRot == self.attribute['rMin']:
                newRot = 0
            
            self.attribute['r'] = newRot
    
    def updateFriction(self):
        if self.attribute['xs'] > 0:
            newxs = self.attribute['xs'] - self.attribute['xFricCoef']
            # Makes sure it doesn't glitch at low speeds
            if newxs < 0: newxs = 0
        elif self.attribute['xs'] < 0:
            newxs = self.attribute['xs'] + self.attribute['xFricCoef']
            if newxs > 0: newxs = 0
        else:
            newxs = 0
        self.attribute['xs'] = newxs
        
        if self.attribute['ys'] > 0:
            newys = self.attribute['ys'] - self.attribute['yFricCoef']
            if newys < 0: newys = 0
        elif self.attribute['ys'] < 0:
            newys = self.attribute['ys'] + self.attribute['yFricCoef']
            if newys > 0: newys = 0
        else:
            newys = 0
        self.attribute['ys'] = newys
        
        if self.attribute['zs'] > 0:
            newzs = self.attribute['zs'] - self.attribute['zFricCoef']
            if newzs < 0: newzs = 0
        elif self.attribute['zs'] < 0:
            newzs = self.attribute['zs'] + self.attribute['zFricCoef']
            if newzs > 0: newzs = 0
        else:
            newzs = 0
        self.attribute['zs'] = newzs
        
        if self.attribute['rs'] > 0:
            newrs = self.attribute['rs'] - self.attribute['rFricCoef']
            if newrs < 0: newrs = 0
        elif self.attribute['rs'] < 0:
            newrs = self.attribute['rs'] + self.attribute['rFricCoef']
            if newrs > 0: newrs = 0
        else:
            newrs = 0
        self.attribute['rs'] = newrs
    
    def updateRect(self):
        self.rect.x = self.attribute['x']
        self.rect.y = self.attribute['y']
    
    def updateAttachments(self):
        for attachment in self.attachmentList:
            attachment.update()
    
    def drawAttachments(self):
        self.attachmentGroup.clear(self.surface, self.image)
        
        # Only update changed areas for speed
        dirty = self.attachmentGroup.draw(self.surface)
        pygame.display.update(dirty)
    
    def removeAttachments(self):
        for attachment in self.attachmentList:
            attachment.remove(self.attachmentGroup)
    
    def checkDestroyConditions(self):
        # Maximum/minimum distance off screen
        if self.attribute['x'] > (game.screenWidth + self.attribute['xDestroyMax']) or self.attribute['x'] < self.attribute['xDestroyMin']:
            self.destruct()
        
        if self.attribute['y'] > (game.screenHeight + self.attribute['yDestroyMax']) or self.attribute['y'] < self.attribute['yDestroyMin']:
            self.destruct()
        
        if self.attribute['z'] > self.attribute['zDestroyMax'] or self.attribute['z'] < self.attribute['zDestroyMin']:
            self.destruct()
            
        if self.attribute['hp'] <= 0:
            # play explode sprite
            self.destruct()
    
    def takeDamage(self, damage):
        if self.attribute['damagable'] == True:
            self.attribute['hp'] -= damage
            print("takeDamage: {} taking {} damage, hp: {}".format(self.attribute['name'], damage, self.attribute['hp']))
            return True
        else:
            return False
    
    def destruct(self):
        self.removeAttachments()
        game.deleteActor(self)
        # Python should remove the object once there are no more references to it
        
    def detectCollisions(self):
        # TODO: Z-Level collision detection
        if self.attribute['primerTicks'] > 0:
            self.attribute['primerTicks'] -= 1
        else:
            if self.attribute['name'] == 'bullet': # Debug: if bullet
                collideList = self.rect.collidelist(game.allSprites)
                print("Collision Detection: {} {} with {}".format(self.attribute['name'], self.actorIndex, collideList))
                
                if collideList != self.actorIndex: # If doesn't collide with self
                    if game.allSprites[collideList].takeDamage(self.attribute['damage']) == True:
                        self.attribute['hp'] -= 1 # In effect, hp is the number of hits a bullet can do
    
    def update(self):
        self.detectCollisions()
        self.checkDestroyConditions()
        self.updateFriction()
        self.runEngine()
        self.updateX(0)
        self.updateY(0)
        self.updateScale()
        self.updateRotation(0)
        self.updateRect()
        self.updateAttachments()
        self.drawAttachments()
        self.image = pygame.transform.rotozoom(self.baseImage, self.attribute['r'], self.attribute['s'])
        
        

class ActorAttachment(pygame.sprite.Sprite):
    """ Class for an actor's items ie. weapons, cosmetic sprites
    """
    def __init__(self, id, name, coord=(0,0,0)):
        pygame.sprite.Sprite.__init__(self) # Call sprite initialiser
        self.loadAttributes(id, name, coord)
        self.setImage()
        self.setRect()
        print("Creating ActorAttachment")
    
    def setImage(self):
        self.actorsImagePath = 'i/Actors'
        imageId = self.attribute['imageId']
        self.attribute['image'] = '{}/{}.png'.format(self.actorsImagePath, imageId)
        self.image = pygame.image.load(self.attribute['image']).convert_alpha()
        self.baseImage = self.image
        self.surface = self.image
        
    def setRect(self):
        self.rect = self.surface.get_rect()
        self.rect.x = self.attribute['x']
        self.rect.y = self.attribute['y']
    
    def loadAttributes(self, id, name, coord):
        self.attribute = self.getAttributes(id)
        self.attribute['name'] = name
        self.attribute['x'] = coord[0]
        self.attribute['y'] = coord[1]
        self.attribute['z'] = coord[2]
    
    def getAttributes(self, id):
        """ Gets properties from JSON file
        """
        # Ideally we don't use game but some form of super() to access getAttributes
        return game.getAttributes(id).copy() # Dicts are passed by reference
        
    def getAttachmentAttribute(self):
        """ Getter for self.attribute
        """
        # TODO: Change the method name to avoid confusion
        return self.attribute
    
    def fire(self, coord, momentum):
        """
        Pew pew pew
        Bullet behaviour can be changed in objects.json
        """
        # Implement fire rate
        print('Firing bullet at coord: {} with momentum: {}'.format(coord, momentum))
        coordOffset = [self.attribute['x'], self.attribute['y'], self.attribute['z'], self.attribute['r']]
        coordOffset[0] = coordOffset[0] + coord[0] # X
        coordOffset[1] = coordOffset[1] + coord[1] # Y
        coordOffset[2] = coordOffset[2] + coord[2] # Z
        coordOffset[3] = coord[3] # Rotation
        
        bulletType = 1 # Expand on this to include logic for picking appropriate bullet for gun type
        
        game.createActor('bullet', bulletType, coordOffset, momentum)
    
    def rotate(self):
        pass
        
    def move(self):
        pass
    
    def update(self):
        self.image = pygame.transform.rotozoom(self.baseImage, self.attribute['r'], self.attribute['s'])

game = Game()
game.main()