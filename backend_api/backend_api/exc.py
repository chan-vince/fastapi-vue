

class EmployeeNotFoundError(Exception):
    pass


class PracticeNotFoundError(Exception):
    pass


class JobTitleNotFoundError(Exception):
    pass


class AddressNotFoundError(Exception):
    pass


class DuplicateEmployeeError(Exception):
    pass


class DuplicateStagingChangePayload(Exception):
    pass


class StagingChangeNotFoundError(Exception):
    pass


class StagingChangeNoEffectError(Exception):
    pass