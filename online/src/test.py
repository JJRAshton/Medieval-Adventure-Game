import backend as bk
import backend.processing as pr

if __name__ == '__main__':
    requester = bk.Requests(bk.TurnNotificationSubscription())
    requester.init(1)


